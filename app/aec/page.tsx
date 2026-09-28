import { demo } from "@/components/data";
import { sitePath } from "@/components/site-path";
import { Callout, SectionHeading, StatusBadge } from "@/components/ui";

const routes = [
  ["/research", "Research", "Problem, questions, objectives and prototype methodology"],
  ["/system", "Database System", "Normalized schema, shared hub and implementation boundary"],
  ["/prototype", "Structural Prototype", "A-B-C beam, MDM trace, results, BMD and SFD"],
  ["/workflow", "Shared-Data Reuse", "Architecture lines, quantities and construction documents"],
  ["/methodology-demo/", "Methodology Demo", "Interactive shared-data AEC methodology demonstrator"],
  ["/structural-demo/", "Structural Solver", "Validated browser structural-analysis solver"],
  ["/graph", "System Graph", "Interactive system and database relationship graph"],
  ["/evidence", "Implementation Evidence", "Public-safe evidence images and QA disclosures"],
  ["/roadmap", "Limitations & Future", "Framework boundaries and future work"],
  ["/thesis", "Thesis Details", "Academic metadata, abstract and cited references"],
] as const;

export default function AecModulePage() {
  return (
    <>
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Research module 01 · AEC / Structural</p>
            <h1>{demo.thesis.title}</h1>
            <p className="hero-summary">
              The original MSc Structural Engineering research website is preserved as this AEC module.
              It presents the normalized relational database prototype, structural validation, shared-data
              reuse and BIM-GIS workflow framework.
            </p>
            <div className="badge-row">
              <StatusBadge status="implemented">Existing AEC system preserved</StatusBadge>
              <StatusBadge status="validated">Structural validation available</StatusBadge>
            </div>
          </div>
          <aside className="truth-panel">
            <p className="kicker">Module identity</p>
            <h2>MSc Structural Engineering</h2>
            <p>Fabin Gurung · Pokhara University · Registration No. 2022-1-90-0005</p>
            <Callout title="Module boundary" tone="blue">
              <p>AEC scientific content remains isolated from the Hydropower research module.</p>
            </Callout>
          </aside>
        </div>
      </section>

      <section className="section section-navy">
        <SectionHeading
          kicker="AEC routes"
          title="Explore the existing thesis system"
          text="The established AEC pages remain available at their original routes and are now grouped under this module entry point."
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
        </div>
      </section>

      <section className="section">
        <a className="text-link" href={sitePath("/")}>← Back to research hub</a>
      </section>
    </>
  );
}
