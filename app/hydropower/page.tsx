import { sitePath } from "@/components/site-path";
import { Callout, NumberedList, PageIntro, SectionHeading, StatusBadge } from "@/components/ui";

const objectives = [
  "Develop a normalized hydropower-infrastructure data model linking sites, assets, geometry, materials, hydrological observations, operations, inspections, environmental/social screening and source documents.",
  "Develop a reproducible GIS/PostGIS and multi-criteria screening workflow for hydropower and pumped-hydropower planning using transparent spatial and infrastructure criteria.",
  "Develop a civil/structural information layer that links geometry, materials, analysis references, verified results and condition records without replacing specialist engineering software.",
  "Map selected BIM/IFC objects and GIS features to common relational asset identifiers and document both successful mappings and limitations.",
  "Design and evaluate a live web-based planning and decision-support prototype with traceable public-safe maps, candidate comparisons and analytical services.",
  "Validate the framework through Nepalese case studies using consistency, traceability, reproducibility, calculation agreement, GIS sensitivity analysis, query accuracy, usability and practitioner review.",
];

export default function HydropowerModulePage() {
  return (
    <>
      <PageIntro
        eyebrow="Research module 02 · Hydropower"
        title="Integrated BIM-GIS and Relational Data Framework for Web-Based Hydropower Planning and Infrastructure Decision Support in Nepal"
        summary="Initial public module derived from the submitted PhD research proposal. The system is intended to connect hydrological, spatial, civil/structural, operational, environmental/social and documentary evidence through stable relational identities and traceable web decision support."
        badges={[
          { status: "framework", label: "PhD research framework" },
          { status: "future", label: "Prototype development lane" },
        ]}
      />

      <section className="section">
        <SectionHeading
          kicker="Research aim"
          title="Connect multidisciplinary hydropower evidence without replacing specialist tools"
          text="The proposed contribution is an information and decision-support framework: verified inputs, outputs, criteria and documents remain traceable to their authoritative sources and specialist analyses."
        />
        <div className="reuse-grid">
          <article><span>01</span><StatusBadge status="framework" /><h3>Hydrology + operations</h3><p>Precipitation, discharge, energy generation, storage and reservoir information where available.</p></article>
          <article><span>02</span><StatusBadge status="framework" /><h3>GIS + planning</h3><p>Terrain, catchments, land use, rivers, access, grid, settlements, hazards and sensitive areas.</p></article>
          <article><span>03</span><StatusBadge status="framework" /><h3>Civil + structural assets</h3><p>Geometry, materials, loads/actions, analysis references, results, inspections and condition records.</p></article>
          <article><span>04</span><StatusBadge status="framework" /><h3>Relational integration</h3><p>Stable asset identifiers, BIM/IFC mappings, GIS geometry links, provenance, units and analysis runs.</p></article>
        </div>
      </section>

      <section className="section section-tinted">
        <SectionHeading kicker="Objectives" title="Initial PhD research work packages" />
        <NumberedList items={objectives} />
      </section>

      <section className="section">
        <div className="boundary-grid">
          <div>
            <SectionHeading
              kicker="Initial case-study context"
              title="Kaligandaki ‘A’ and broader Nepalese screening"
              text="Kaligandaki ‘A’ near Mirmi in Syangja is identified in the proposal as an initial operations and water-resource case, supported by the applicant’s prior cleaned 2019–2023 research dataset. Additional Nepalese areas may support hydropower and PHES spatial screening where public or permission-cleared data are available."
            />
          </div>
          <div>
            <Callout title="Public research boundary" tone="amber">
              <p>
                Site-suitability outputs are pre-feasibility research only. They do not replace statutory ESIA,
                detailed feasibility, field surveys, geotechnical investigation, formal approval, or specialist
                hydrological and structural analysis.
              </p>
            </Callout>
          </div>
        </div>
      </section>

      <section className="section section-navy">
        <SectionHeading
          kicker="Planned system"
          title="Hydropower module roadmap"
          text="This first release establishes the research identity and architecture. Data schemas, maps, case-study evidence, analysis services and validation pages can be added as governed research outputs become ready for public release."
        />
        <div className="route-grid">
          <article className="route-card"><span>01</span><h3>Research Proposal</h3><p>Current public-safe research title, aim, objectives, methodology and limitations.</p></article>
          <article className="route-card"><span>02</span><h3>Hydropower Data Model</h3><p>Future normalized PostgreSQL/PostGIS schema for sites, assets, observations, evidence and provenance.</p></article>
          <article className="route-card"><span>03</span><h3>GIS / PHES Screening</h3><p>Future reproducible terrain and multi-criteria candidate screening with sensitivity records.</p></article>
          <article className="route-card"><span>04</span><h3>Case Studies</h3><p>Future permission-cleared operational, spatial and infrastructure validation evidence.</p></article>
        </div>
      </section>

      <section className="section">
        <p className="source-note"><span>Source disclosure</span>Submitted Pokhara University PhD Research Proposal (Form E), dated 22 September 2026. Private Drive administration and application records are not published.</p>
        <a className="text-link" href={sitePath("/")}>← Back to research hub</a>
      </section>
    </>
  );
}
