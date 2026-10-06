import { sitePath } from "@/components/site-path";
import { SectionHeading, StatusBadge } from "@/components/ui";
import { projectPath, researchProjects } from "@/components/research-directory";

const modules = [
  {
    href: "/aec/",
    code: "AEC / STRUCTURAL",
    title: "MSc Structural Engineering Research",
    description:
      "Normalized relational data, BIM-GIS workflow automation, structural-analysis validation and shared-data reuse.",
    meta: "Pokhara University · MSc Structural Engineering",
    status: "Live research system",
  },
  {
    href: "/hydropower/",
    code: "HYDROPOWER",
    title: "Hydropower Research",
    description:
      "Integrated BIM-GIS, relational/spatial data and web-based hydropower planning and infrastructure decision support in Nepal.",
    meta: "Pokhara University · PhD research",
    status: "Research module initiated",
  },
] as const;

export default function ResearchHubPage() {
  return (
    <>
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Fabin Gurung</p>
            <h1>Engineering Research System</h1>
            <p className="hero-summary">A shared home for theses, engineering studies and energy research.</p>
            <div className="badge-row">
              <StatusBadge status="implemented">AEC / Structural</StatusBadge>
              <StatusBadge status="framework">Hydropower</StatusBadge>
            </div>
          </div>
          <aside className="truth-panel">
            <p className="kicker">Research hub</p>
            <h2>Choose a research system</h2>
            <p>
              Browse the project directory or open an established research module.
              Each project keeps its own scientific evidence and development path.
            </p>
            <a className="directory-link" href={sitePath('/projects/')}>Explore the research directory →</a>
          </aside>
        </div>
      </section>

      <section className="section section-navy">
        <SectionHeading
          kicker="Research systems"
          title="Established research modules"
          text="The website shell is shared; scientific content and source chains remain separated by research domain."
        />
        <div className="route-grid">
          {modules.map((module, index) => (
            <a className="route-card" href={sitePath(module.href)} key={module.href}>
              <span>{String(index + 1).padStart(2, "0")} · {module.code}</span>
              <h3>{module.title}</h3>
              <p>{module.description}</p>
              <small>{module.meta} · {module.status}</small>
              <b aria-hidden="true">↗</b>
            </a>
          ))}
        </div>
      </section>
      <section className="section">
        <SectionHeading kicker="Project directory" title="Research across projects" text="Stable project addresses connect theses, structural studies and energy investigations." />
        <div className="research-directory-grid">
          {researchProjects.map(project => <a className="research-project-card" key={project.project_id} href={sitePath(projectPath(project.slug))}>
            <span className="kicker">{project.category}</span><h3>{project.label}</h3><p>{project.summary}</p>
            <small>{project.status === 'PUBLIC_MODULE_AVAILABLE' ? 'Public module available' : 'Directory entry · publication pending'}</small>
          </a>)}
        </div>
      </section>
    </>
  );
}
