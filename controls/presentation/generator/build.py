from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from a9_presentation_validator import load_json, validate_content, sha256_file
from a9_presentation_generator import build_pdf, build_pptx
from a9_render_qa import qa_release
from a9_semantic_checker import check_semantics
from a9_literature_table import expand_literature_tables
from a9_methodology_flow import expand_methodology_flows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--content", required=True)
    ap.add_argument("--theme", default="theme.default.json")
    ap.add_argument("--out-dir", default="build")
    ap.add_argument("--production", action="store_true")
    ap.add_argument("--no-pptx", action="store_true")
    ap.add_argument("--evidence-map", help="current project-specific admitted evidence map JSON")
    ap.add_argument("--fixture", action="store_true", help="synthetic smoke-test only; cannot certify researcher work")
    args=ap.parse_args()
    content_path=Path(args.content).resolve(); theme_path=Path(args.theme).resolve(); out=Path(args.out_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    content=load_json(content_path); theme=load_json(theme_path)
    v=validate_content(content,theme,content_path.parent)
    (out/"validation.json").write_text(json.dumps(v,indent=2),encoding="utf-8")
    if not v["ok"]:
        print(json.dumps(v,indent=2)); return 2
    if args.fixture and args.production:
        print("Fixture cannot be certified production"); return 2
    e_map = load_json(args.evidence_map) if args.evidence_map else None
    sem = check_semantics(content, e_map, mode="fixture" if args.fixture else "researcher")
    (out/"semantic_validation.json").write_text(json.dumps(sem,indent=2),encoding="utf-8")
    if not sem["ok"]:
        print(json.dumps(sem,indent=2)); return 2
    pdf=out/"presentation.pdf"; pptx=out/"presentation.pptx"
    # resolve asset paths relative to content source so renderers get concrete paths
    logo_p=Path(str(content.get("metadata",{}).get("logo",""))) if content.get("metadata",{}).get("logo") else None
    if logo_p is not None and not logo_p.is_absolute():
        content["metadata"]["logo"]=str((content_path.parent/logo_p).resolve())
    for slide in content["slides"]:
        if slide["type"]=="figure":
            p=Path(slide["figure"]["path"])
            if not p.is_absolute(): slide["figure"]["path"]=str((content_path.parent/p).resolve())
        if slide["type"]=="two_figures":
            for obj in slide.get("figures",[]):
                p=Path(obj["path"])
                if not p.is_absolute(): obj["path"]=str((content_path.parent/p).resolve())
    content = expand_methodology_flows(expand_literature_tables(content))
    build_pdf(content,theme,pdf,production=args.production)
    if not args.no_pptx:
        build_pptx(content,theme,pptx,production=args.production)
    report=qa_release(pdf, None if args.no_pptx else pptx, out/"renders", out/"montage.jpg", out/"qa_release.json")
    manifest={
        "generator_version":theme["system"].get("name"),
        "control_version":theme["system"].get("control_version"),
        "control_drive_id":theme["system"]["control_drive_id"],
        "qa_drive_id":theme["system"].get("qa_drive_id"),
        "rule_registry_drive_id":theme["system"].get("rule_registry_drive_id"),
        "content_sha256":sha256_file(content_path),
        "theme_sha256":sha256_file(theme_path),
        "validation":"PASS",
        "semantic_validation": "FIXTURE_ONLY" if args.fixture else "PROVENANCE_LINKAGE_PASS_HUMAN_SCIENCE_REVIEW_REQUIRED",
        "pdf_sha256":report["pdf"]["sha256"],
        "pptx_sha256":report["pptx"]["sha256"] if report["pptx"] else None,
        "render_count":report["pdf"]["pages"],
        "literature_matrix_pages":sum(s.get("type")=="literature_table" for s in content["slides"]),
        "methodology_flow_pages":sum(s.get("type")=="methodology_flow" for s in content["slides"]),
        "literature_matrix_evidence_policy":"SOURCE_AND_FINDING_LOCATOR_REQUIRED__HUMAN_REVIEW_PENDING",
        "production_requested":bool(args.production),
        "title_logo_size_in":content.get("metadata",{}).get("title_logo_size_in",theme.get("branding",{}).get("title_logo_default_in")),
        "supervisor_present":bool((content.get("metadata",{}).get("supervisor") or {}).get("name")),
        "co_supervisor_count":len(content.get("metadata",{}).get("co_supervisors") or [])
    }
    (out/"release_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
