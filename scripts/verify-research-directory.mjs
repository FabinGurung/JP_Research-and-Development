import assert from 'node:assert/strict';
import fs from 'node:fs';

const catalog = JSON.parse(fs.readFileSync('data/research-projects.json', 'utf8'));
const ids = new Set();
const slugs = new Set();
for (const project of catalog.projects) {
  assert.match(project.project_id, /^PROJ-\d{6}$/);
  assert.ok(!ids.has(project.project_id), 'Duplicate permanent project identity');
  assert.ok(!slugs.has(project.slug), 'Duplicate project slug');
  assert.match(project.slug, /^[a-z0-9]+(?:-[a-z0-9]+){2,}$/);
  assert.ok(project.label.trim().split(/\s+/).length >= 3, 'Use at least three meaningful words');
  assert.equal(project.scientific_state, 'NOT_ASSERTED');
  assert.equal(project.publication, 'PUBLIC_METADATA_ONLY');
  assert.ok(project.status === 'PUBLIC_MODULE_AVAILABLE' ? project.route : project.route === null);
  ids.add(project.project_id); slugs.add(project.slug);
}
const publicationText = JSON.stringify(catalog);
assert.doesNotMatch(publicationText, /docs\.google\.com|drive\.google\.com|CP113|DISC-SEQ|LATEX-SEQ/);
const current = JSON.parse(fs.readFileSync('CURRENT.json', 'utf8'));
assert.equal(current.a9_repository.provider_id, null);
assert.equal(current.a9_repository.status, 'NOT_PROVISIONED');
console.log(`Research directory identities, slugs and public boundary: PASS (${ids.size} projects)`);
