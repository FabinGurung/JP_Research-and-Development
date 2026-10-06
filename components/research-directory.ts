import catalog from '@/data/research-projects.json';

export const researchProjects = catalog.projects;
export const directoryAuthority = catalog.authority;

export function projectPath(slug: string) {
  return `/projects/${slug}/`;
}
