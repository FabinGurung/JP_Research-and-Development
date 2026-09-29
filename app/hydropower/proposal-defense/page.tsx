import { sitePath } from "@/components/site-path";

const DRIVE_FILE_ID = "1E_uN5KD2R-jfkeKGKJUlu81G_cEhdtoy";
const DRIVE_VIEW_URL = `https://drive.google.com/file/d/${DRIVE_FILE_ID}/view?usp=drivesdk`;
const DRIVE_PREVIEW_URL = `https://drive.google.com/file/d/${DRIVE_FILE_ID}/preview`;

const relatedResources = [
  {
    label: "GOOGLE DRIVE FOLDER",
    title: "Proposal-defense release folder",
    description: "Open the shared Drive folder containing the governed proposal-defense release files.",
    href: "https://drive.google.com/drive/folders/1z0pHNTVX9pIIqMY9xxKg_C-GkNllA1Q0",
  },
  {
    label: "PDF",
    title: "Fabin Gurung PhD Proposal Defense · SEQ16",
    description: "Open the released PDF directly in Google Drive.",
    href: "https://drive.google.com/file/d/1LBNbLlrTGXI_ldEIcCSJ47XeTO7PMpwv/view?usp=drivesdk",
  },
  {
    label: "PRESENTATION / PPTX",
    title: "Editable proposal-defense presentation · SEQ16",
    description: "Open the compatible PPTX presentation in the Google Slides interface.",
    href: "https://docs.google.com/presentation/d/1DIMr8WbeyBp554N66VxGsB7GWU3GBu1l/edit?usp=drivesdk&ouid=103752966999827673119&rtpof=true&sd=true",
  },
];

export default function HydropowerProposalDefensePage() {
  return (
    <main style={{ minHeight: "100vh", background: "#eef3f7", color: "#13283a" }}>
      <header style={{ background: "#071f34", color: "#eef7fc", padding: "14px 18px", display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
        <div style={{ marginRight: "auto" }}>
          <strong style={{ display: "block", fontSize: "1rem" }}>Hydropower · PhD Proposal Defense</strong>
          <span style={{ color: "#9db7c9", fontSize: ".78rem" }}>Live Google Drive PDF viewer</span>
        </div>
        <a href={sitePath("/hydropower/")} style={{ color: "#eef7fc", textDecoration: "none", border: "1px solid #3c5b70", borderRadius: 8, padding: "7px 10px", fontSize: ".78rem" }}>← Hydropower</a>
        <a href={DRIVE_VIEW_URL} target="_blank" rel="noopener noreferrer" style={{ color: "#eef7fc", textDecoration: "none", border: "1px solid #5c8199", borderRadius: 8, padding: "7px 10px", fontSize: ".78rem", background: "#124c70" }}>Open displayed PDF in Google Drive ↗</a>
      </header>

      <section style={{ padding: "18px", maxWidth: 1500, margin: "0 auto" }}>
        <div style={{ marginBottom: 12, background: "#fff", border: "1px solid #d6e0e8", borderRadius: 12, padding: "12px 14px" }}>
          <div style={{ fontSize: ".68rem", fontWeight: 800, letterSpacing: ".08em", textTransform: "uppercase", color: "#52738a", marginBottom: 5 }}>Drive-backed research document</div>
          <h1 style={{ margin: "0 0 5px", fontSize: "1.25rem" }}>Integrated Hydropower Evidence for Decision Support in Nepal</h1>
          <p style={{ margin: 0, color: "#657587", lineHeight: 1.45, fontSize: ".86rem" }}>PhD Research Proposal Defense · Fabin Gurung · Pokhara University · 23 pages. This page displays the supplied Google Drive PDF directly; the website does not duplicate or rewrite the document.</p>
        </div>

        <div style={{ background: "#fff", border: "1px solid #cfdbe4", borderRadius: 12, overflow: "hidden", boxShadow: "0 8px 28px rgba(13,42,61,.10)" }}>
          <iframe
            src={DRIVE_PREVIEW_URL}
            title="Fabin Gurung PhD Proposal Defense PDF"
            style={{ width: "100%", height: "calc(100vh - 220px)", minHeight: 720, border: 0, display: "block" }}
            allow="autoplay"
          />
        </div>

        <p style={{ margin: "10px 2px 0", color: "#6a7986", fontSize: ".76rem", lineHeight: 1.45 }}>
          If the embedded Google viewer is blocked by a browser privacy setting, use “Open displayed PDF in Google Drive” above. Source file ID: {DRIVE_FILE_ID}.
        </p>

        <section style={{ marginTop: 18, background: "#fff", border: "1px solid #d6e0e8", borderRadius: 12, padding: "14px" }}>
          <div style={{ fontSize: ".68rem", fontWeight: 800, letterSpacing: ".08em", textTransform: "uppercase", color: "#52738a", marginBottom: 5 }}>Other linked proposal-defense resources</div>
          <h2 style={{ margin: "0 0 6px", fontSize: "1.06rem" }}>Google Drive release links</h2>
          <p style={{ margin: "0 0 12px", color: "#657587", lineHeight: 1.45, fontSize: ".82rem" }}>These links stay on Google Drive so the live source files remain separate from the GitHub website.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 10 }}>
            {relatedResources.map((resource) => (
              <a
                key={resource.href}
                href={resource.href}
                target="_blank"
                rel="noopener noreferrer"
                style={{ display: "block", textDecoration: "none", color: "#16384d", border: "1px solid #cbd9e2", borderRadius: 10, padding: "12px", background: "#f8fbfd" }}
              >
                <span style={{ display: "block", fontSize: ".64rem", fontWeight: 850, letterSpacing: ".07em", color: "#2b6d91", marginBottom: 5 }}>{resource.label}</span>
                <strong style={{ display: "block", fontSize: ".9rem", marginBottom: 5 }}>{resource.title}</strong>
                <span style={{ display: "block", color: "#667987", fontSize: ".76rem", lineHeight: 1.4 }}>{resource.description}</span>
                <span style={{ display: "block", marginTop: 8, fontSize: ".74rem", fontWeight: 800, color: "#0d638e" }}>Open resource ↗</span>
              </a>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
