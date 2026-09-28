import { sitePath } from "@/components/site-path";
import { Callout, SectionHeading, StatusBadge } from "@/components/ui";

const modules = [
  {
    href: "/aec/",
    code: "AEC",
    title: "AEC / Structural Research System",
    description:
      "MSc Structural Engineering thesis system covering normalized relational data, BIM-GIS workflow automation, structural-analysis validation and shared-data reuse.",
    meta: "MSc Structural Engineering · Pokhara University",
  },
  {
    href: "/hydropower/",
    code: "HYDRO",
    title: "Hydropower Research System",
    description:
      "PhD research system for integrated BIM-GIS, relational/spatial data and web-based hydropower planning and infrastructure decision support in Nepal.",
    meta: "PhD research proposal · Hydropower planning + infrastructure",
  },
] as const;

export default function ResearchHubPage() {
  return (
    <>
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Fabin Gurung · Engineering research hub</p>
            <h1>One research website. Multiple engineering systems.</h1>
            <p className="hero-summary">
              A shared public research portal that keeps each research domain separate while reusing
              one governed static publishing architecture. The AEC thesis remains intact as the first
              module; Hydropower is now the second module.
            </p>
            <div className="badge-row">
              <StatusBadge status="implemented">AEC module live</StatusBadge>
              <StatusBadge status="framework">Hydropower module initiated</StatusBadge>
            </div>
          </div>
          <aside className="truth-panel">
            <p className="kicker">Publishing model</p>
            <h2>Shared shell, isolated research truth</h2>
            <div className="truth-flow">
              <div><span>01</span><strong>Choose a research system</strong><small>AEC or Hydropower</small></div>
              <div><span>02</span><strong>Enter its governed module</strong><small>Domain-specific evidence and routes</small></div>
              <div><span>03</span><strong>Publish public-safe outputs</strong><small>Static GitHub Pages export</small></div>
            </div>
          </aside>
        </div>
      </section>

      <section className="section section-navy">
        <SectionHeading
          kicker="Research systems"
          title="Select a module"
          text="Each module has its own research scope, evidence chain and development roadmap while sharing the same website infrastructure."
        />
        <div className="route-grid">
          {modules.map((module, index) => (
            <a className="route-card" href={sitePath(module.href)} key={module.href}>
              <span>{String(index + 1).padStart(2, "0")} · {module.code}</span>
              <h3>{module.title}</h3>
              <p>{module.description}</p>
              <small>{module.meta}</small>
              <b aria-hidden="true">↗</b>
            </a>
          ))}
        </div>
      </section>

      <section className="section">
        <Callout title="Research isolation rule" tone="blue">
          <p>
            AEC and Hydropower share the publishing shell only. Their scientific claims, data,
            calculations and source chains remain independently governed and are not mixed across modules.
          </p>
        </Callout>
      </section>
    </>
  );
}
