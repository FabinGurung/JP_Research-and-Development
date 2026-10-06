import { directoryAuthority, projectPath, researchProjects } from '@/components/research-directory';
import { sitePath } from '@/components/site-path';
import { PageIntro, SectionHeading } from '@/components/ui';

export const metadata = { title: 'Research directory' };

export default function ResearchDirectoryPage() {
  return <>
    <PageIntro eyebrow="Research directory" title="Find a research project"
      summary="Theses, structural studies, building workflows and energy investigations, with a stable address for each project." />
    <section className="section">
      <SectionHeading kicker="Projects" title="Five research entries" text={directoryAuthority} />
      <div className="research-directory-grid">
        {researchProjects.map(project => <a className="research-project-card" key={project.project_id} href={sitePath(projectPath(project.slug))}>
          <span className="kicker">{project.category}</span>
          <h3>{project.label}</h3>
          <p>{project.summary}</p>
          <small>{project.status === 'PUBLIC_MODULE_AVAILABLE' ? 'Public module available' : 'Directory entry · publication pending'}</small>
          <span className="project-identity">{project.project_id}</span>
        </a>)}
      </div>
      <p className="source-note"><span>Directory source</span>Names and scope summaries follow the supplied research architecture plan. These entries do not assert manuscript, dataset or review status.</p>
    </section>
  </>;
}
