import { demo } from "@/components/data";
import { sitePath } from "@/components/site-path";
import { Callout, SectionHeading, StatusBadge } from "@/components/ui";

const routes = [
  ["/research", "Thesis / Database Research", "Problem, questions, objectives, normalized relational data and prototype methodology"],
  ["/system", "Database System", "Normalized schema, shared hub and implementation boundary"],
  ["/prototype", "Structural Prototype", "A-B-C beam, MDM trace, results, BMD and SFD"],
  ["/workflow", "Methodology / Shared-Data Reuse", "Architecture lines, quantities, construction documents and reusable data workflow"],
  ["/methodology-demo/", "Methodology Demo", "Interactive shared-data AEC methodology demonstrator"],
  ["/graph", "System Graph", "Interactive system and database relationship graph"],
  ["/evidence", "Implementation Evidence", "Public-safe evidence images and QA disclosures"],
  ["/roadmap", "Limitations & Future", "Framework boundaries and future work"],
  ["/thesis", "Thesis Details", "Academic metadata, abstract and cited references"],
] as const;

const structuralEngineUrl = "https://github.com/FabinGurung/JP_Structural_Analysis";

export default function AecModulePage() {
  return (
    <>
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Research module 01 · AEC / Structural</p>
            <h1>{demo.thesis.title}</h1>
            <p className="hero-summary">
              The MSc Structural Engineering research system is preserved here as the AEC / Structural
              research module. It presents the normalized relational database prototype, methodology,
              evidence, structural-validation research and BIM-GIS workflow framework.
            </p>
            <div className="badge-row">
              <StatusBadge status="implemented">AEC research preserved</StatusBadge>
              <StatusBadge status="validated">Structural validation available</StatusBadge>
            </div>
          </div>
          <aside className="truth-panel">
            <p className="kicker">Module identity</p>
            <h2>MSc Structural Engineering</h2>
            <p>Fabin Gurung · Pokhara University · Registration No. 2022-1-90-0005</p>
            <Callout title="Product boundary" tone="blue">
              <p>
                Research evidence stays in this R&amp;D module. The executable Structural Analysis / SAR
                product now has its own repository: JP_Structural_Analysis.
              </p>
            </Callout>
          </aside>
        </div>
      </section>

      <section className="section section-navy">
        <SectionHeading
          kicker="AEC / Structural research"
          title="Research, methodology, evidence and structural-analysis handoff"
          text="The established thesis pages remain under the R&D hub. The dedicated structural-analysis engine is separated into JP_Structural_Analysis so solver development cannot replace this research homepage."
        />
        <div className="route-grid">
          {routes.map(([href, title, description], index) => (
            <a className="route-card" href={sitePath(href)} key={href}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{title}</h3>
              <p>{description}</p>
              <b aria-hidden="true">↗</b>
            </a>
          ))}
          <a className="route-card" href={structuralEngineUrl}>
            <span>ENGINE</span>
            <h3>JP Structural Analysis</h3>
            <p>Dedicated OpenSees/SAR structural-analysis engine repository, separated from the R&amp;D publication hub.</p>
            <b aria-hidden="true">↗</b>
          </a>
          <a className="route-card" href={sitePath("/structural-demo/")}>
            <span>LEGACY RESEARCH DEMO</span>
            <h3>Structural Solver Research Snapshot</h3>
            <p>Preserved public research/validation demonstrator from the earlier R&amp;D lineage; it is not the canonical product engine.</p>
            <b aria-hidden="true">↗</b>
          </a>
        </div>
      </section>

      <section className="section">
        <a className="text-link" href={sitePath("/")}>← Back to research hub</a>
      </section>
    </>
  );
}
