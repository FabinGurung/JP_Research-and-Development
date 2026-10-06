import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { projectPath, researchProjects } from '@/components/research-directory';
import { sitePath } from '@/components/site-path';
import { Callout, PageIntro, SectionHeading } from '@/components/ui';

export const dynamicParams = false;
export function generateStaticParams() {
  return researchProjects.map(project => ({ slug: project.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const project = researchProjects.find(item => item.slug === slug);
  return { title: project?.label ?? 'Research project' };
}

export default async function ProjectPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const project = researchProjects.find(item => item.slug === slug);
  if (!project) notFound();
  return <>
    <PageIntro eyebrow={`${project.category} · ${project.project_id}`} title={project.label} summary={project.summary} />
    <section className="section">
      <div className="reading-grid">
        <SectionHeading kicker="Research record" title="A stable project address" />
        <div className="prose-panel">
          <p>This entry identifies the project and its public research route. Original sources, working documents and scientific releases remain in the project's Google Drive authorities.</p>
          <dl className="project-details">
            <dt>Permanent identity</dt><dd>{project.project_id}</dd>
            <dt>Research category</dt><dd>{project.category}</dd>
            <dt>Publication</dt><dd>{project.status === 'PUBLIC_MODULE_AVAILABLE' ? 'Public research module available below' : 'Directory metadata; scientific publication pending'}</dd>
          </dl>
          {project.route ? <a className="directory-link" href={sitePath(project.route)}>Open the public research module →</a> :
            <Callout title="Research content pending" tone="gray"><p>No manuscript, numerical results or private evidence are published on this page. Add reviewed public material after the owning research lane verifies its sources.</p></Callout>}
        </div>
      </div>
      <p className="source-note"><span>Directory source</span>{project.source}</p>
      <div className="directory-actions">
        <a href={sitePath('/projects/')}>← All research projects</a>
        <a href={sitePath('/governance/')}>How the research records are managed</a>
      </div>
    </section>
    <section className="section section-tinted">
      <SectionHeading kicker="Explore" title="Related research directory" />
      <div className="research-directory-grid">
        {researchProjects.filter(item => item.category === project.category && item.project_id !== project.project_id).map(item =>
          <a className="research-project-card" key={item.project_id} href={sitePath(projectPath(item.slug))}><h3>{item.label}</h3><p>{item.summary}</p></a>)}
        <a className="research-project-card" href={sitePath('/projects/')}><h3>Browse all projects</h3><p>Explore the full research directory across disciplines.</p></a>
      </div>
    </section>
  </>;
}
