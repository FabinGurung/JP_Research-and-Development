import { sitePath } from "@/components/site-path";

const DRIVE_FILE_ID = "1E_uN5KD2R-jfkeKGKJUlu81G_cEhdtoy";
const DRIVE_VIEW_URL = `https://drive.google.com/file/d/${DRIVE_FILE_ID}/view?usp=drivesdk`;
const DRIVE_PREVIEW_URL = `https://drive.google.com/file/d/${DRIVE_FILE_ID}/preview`;

export default function HydropowerProposalDefensePage() {
  return (
    <main style={{ minHeight: "100vh", background: "#eef3f7", color: "#13283a" }}>
      <header style={{ background: "#071f34", color: "#eef7fc", padding: "14px 18px", display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
        <div style={{ marginRight: "auto" }}>
          <strong style={{ display: "block", fontSize: "1rem" }}>Hydropower · PhD Proposal Defense</strong>
          <span style={{ color: "#9db7c9", fontSize: ".78rem" }}>Live Google Drive PDF viewer</span>
        </div>
        <a href={sitePath("/hydropower/")} style={{ color: "#eef7fc", textDecoration: "none", border: "1px solid #3c5b70", borderRadius: 8, padding: "7px 10px", fontSize: ".78rem" }}>← Hydropower</a>
        <a href={DRIVE_VIEW_URL} target="_blank" rel="noopener noreferrer" style={{ color: "#eef7fc", textDecoration: "none", border: "1px solid #5c8199", borderRadius: 8, padding: "7px 10px", fontSize: ".78rem", background: "#124c70" }}>Open in Google Drive ↗</a>
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
          If the embedded Google viewer is blocked by a browser privacy setting, use “Open in Google Drive” above. Source file ID: {DRIVE_FILE_ID}.
        </p>
      </section>
    </main>
  );
}
