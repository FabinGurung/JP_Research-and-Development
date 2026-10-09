#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def load(p):
    try:return json.loads((ROOT/p).read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{p}: {e}"); return {}
researchers=load("registry/researchers.json")
websites=load("registry/websites.json")
debts=load("registry/debts.json")
manoj_audit=load("registry/drive-audits/02-thesis/manoj-bhandari.json")
binay_audit=load("registry/drive-audits/02-thesis/binay-karki.json")
avishek_audit=load("registry/drive-audits/02-thesis/avishek-kumar-mandal.json")
root_rescan=load("registry/drive-audits/02-thesis/root-rescan-20261008.json")
audit_batch_slugs=("rural-road-maintenance","safal-dawadi","saugat-paneru","nabin-bista","krishna-kumar-gupta","shisheer-kc","sunil-rana","fabin-gurung","master-index")
audit_batch={slug:load(f"registry/drive-audits/02-thesis/{slug}.json") for slug in audit_batch_slugs}
branches=load("registry/branch-registry.json")
branch_inventory=load("registry/branch-inventory.json")
roadmap=load("registry/roadmap.json")
policy=load("controls/repository.control.json")
latex_policy=load("controls/latex.control.json")
safal_policy=load("controls/projects/safal-dawadi.latex.json")
required=["README.md","CURRENT.json","A7_MODULE.json","registry/researchers.json","registry/websites.json","registry/debts.json","registry/drive-audits/02-thesis/manoj-bhandari.json","registry/drive-audits/02-thesis/binay-karki.json","registry/drive-audits/02-thesis/avishek-kumar-mandal.json","registry/drive-audits/02-thesis/root-rescan-20261008.json","registry/drive-audits/02-thesis/rural-road-maintenance.json","registry/drive-audits/02-thesis/safal-dawadi.json","registry/drive-audits/02-thesis/saugat-paneru.json","registry/drive-audits/02-thesis/nabin-bista.json","registry/drive-audits/02-thesis/krishna-kumar-gupta.json","registry/drive-audits/02-thesis/shisheer-kc.json","registry/drive-audits/02-thesis/sunil-rana.json","registry/drive-audits/02-thesis/fabin-gurung.json","registry/drive-audits/02-thesis/master-index.json","registry/branch-registry.json","controls/repository.control.json","controls/discussion.control.json","controls/latex.control.json","controls/presentation.control.json","controls/website.control.json","schemas/researchers.schema.json","scripts/build_site.py","scripts/validate_repo.py","web/styles.css",".github/workflows/validate.yml",".github/workflows/pages.yml"]
required += ["controls/projects/safal-dawadi.latex.json","docs/LATEX_CONTROL_OWNERSHIP.md","scripts/latex/safal_build.py",".github/workflows/safal-latex.yml"]
for p in required:
    if not (ROOT/p).is_file(): errors.append(f"missing {p}")
rows=researchers.get("researchers",[])
if len(rows)!=11: errors.append(f"expected 11 researchers, got {len(rows)}")
ids=set(); slugs=set(); lane_names=set()
for r in rows:
    if r.get("researcher_id") in ids: errors.append("duplicate researcher_id")
    if r.get("slug") in slugs: errors.append("duplicate slug")
    ids.add(r.get("researcher_id")); slugs.add(r.get("slug"))
    status=r.get("qa_status")
    if status not in ("HOLD_HUMAN_QA","TITLE_VERIFIED_OTHER_POINTERS_HOLD"): errors.append(f"{r.get('slug')}: unsupported QA status {status}")
    if status=="HOLD_HUMAN_QA":
        if r.get("topic_title") is not None or r.get("topic_short_name") is not None: errors.append(f"{r.get('slug')}: topic published before QA")
    if status=="TITLE_VERIFIED_OTHER_POINTERS_HOLD":
        if not r.get("topic_title"): errors.append(f"{r.get('slug')}: verified title status without title")
    for kind in ("discussion","latex","presentation"):
        b=r.get("lanes",{}).get(kind,{}).get("branch")
        exp=f"researcher/{r.get('slug')}/{kind}"
        if b!=exp: errors.append(f"{r.get('slug')}: {kind} branch mismatch")
        if b in lane_names: errors.append(f"duplicate lane {b}")
        lane_names.add(b)
if roadmap.get("baseline",{}).get("registered_researchers")!=11 or not roadmap.get("developed") or not roadmap.get("next"):
    errors.append("R&D roadmap missing or wrong researcher scope")
observed_branch_rows=branch_inventory.get("branches",[])
if branch_inventory.get("observed_branch_count") != len(observed_branch_rows) or len(observed_branch_rows)<100:
    errors.append("branch inventory count invalid or unexpectedly small")
if len({x.get("name") for x in observed_branch_rows}) != len(observed_branch_rows):
    errors.append("branch inventory contains duplicate refs")
if not {"main","snapshot/20261009/rnd-main/v001-pre-rose-dawn"} <= {x.get("name") for x in observed_branch_rows}:
    errors.append("production/initial rollback refs missing from branch inventory")
if len([x for x in observed_branch_rows if x.get("category")=="researcher-template"])!=33:
    errors.append("legacy 33 researcher lanes must not be falsely promoted to source")
if len([x for x in observed_branch_rows if x.get("category")=="resource"])!=17:
    errors.append("17 versioned resource branches missing from inventory")
if latex_policy.get("source_code")!="controls/latex/tower.json" or latex_policy.get("status")!="ALIAS_ROUTING_ONLY_NOT_SECOND_TOWER":
    errors.append("legacy LaTeX alias is not a single-tower route")
if safal_policy.get("researcher_id")!="RSH-010":
    errors.append("Safal scoped LaTeX researcher mismatch")
if safal_policy.get("branches",{}).get("shared_latex_control_release")!="resource/control/latex/v004-20261009":
    errors.append("shared LaTeX v002 version not linked from Safal")
if safal_policy.get("gates",{}).get("source_admission") not in ("HOLD","VERIFIED"):
    errors.append("Safal source status must be HOLD or verified Git-source admission")
if safal_policy.get("gates",{}).get("source_admission")=="VERIFIED" and not (ROOT/"researchers/safal-dawadi/latex/manuscript/main.tex").is_file():
    errors.append("Safal source verified without committed manuscript main.tex")
if safal_policy.get("original_drive",{}).get("main_ack_reported")!=5:
    errors.append("Safal Main Library cursor not preserved")
if len(lane_names)!=33: errors.append("expected 33 researcher lanes")
reg={x.get("branch") for x in branches.get("active_researcher_lanes",[])}
if reg!=lane_names: errors.append("branch registry active lanes != researcher registry")
if len(branches.get("archived_legacy",[]))!=45: errors.append("expected 45 original non-main legacy refs")
for row in branches.get("archived_legacy",[]):
    if not str(row.get("branch","")).startswith("archive/"): errors.append(f"archived ref missing archive/ prefix: {row.get('branch')}")
for row in branches.get("migration_refs",[]):
    if str(row.get("status","")).startswith("ARCHIVED") and not str(row.get("branch","")).startswith("archive/"): errors.append(f"archived migration ref missing archive/ prefix: {row.get('branch')}")
website_rows=websites.get("websites",[])
website_branches=set()
for w in website_rows:
    rid=w.get("researcher_id")
    match=next((r for r in rows if r.get("researcher_id")==rid),None)
    if not match:
        errors.append(f"website {w.get('website_id')}: unknown researcher")
        continue
    exp=f"researcher/{match.get('slug')}/website/{w.get('module_slug')}"
    if w.get("branch")!=exp: errors.append(f"website {w.get('website_id')}: branch mismatch")
    if w.get("branch") in website_branches: errors.append(f"duplicate website branch {w.get('branch')}")
    website_branches.add(w.get("branch"))
    if not str(w.get("route","")).startswith("/"): errors.append(f"website {w.get('website_id')}: invalid route")
registered_web={x.get("branch") for x in branches.get("active_website_modules",[])}
if registered_web!=website_branches: errors.append("branch registry website modules != website registry")
debt_rows=debts.get("debts",[])
debt_ids=set()
for d in debt_rows:
    did=d.get("debt_id")
    if not did or did in debt_ids: errors.append(f"invalid/duplicate debt_id {did}")
    debt_ids.add(did)
    if d.get("status") not in ("OPEN","HOLD","CLOSED"): errors.append(f"{did}: unsupported debt status")
    if d.get("scope") not in ("RESEARCHER","REPOSITORY"): errors.append(f"{did}: unsupported debt scope")
    if d.get("scope")=="RESEARCHER":
        rid=d.get("researcher_id")
        if rid not in ids: errors.append(f"{did}: unknown researcher_id {rid}")
    if d.get("audit_slug") and d.get("audit_slug") not in ("manoj-bhandari","avishek-kumar-mandal",*audit_batch_slugs):
        errors.append(f"{did}: unregistered audit_slug")
if manoj_audit.get("researcher_workflow",{}).get("registered_in_repository") is not False:
    errors.append("Manoj audit cannot be promoted as a registered researcher without independent authority")
if binay_audit.get("researcher_id")!="RSH-006":
    errors.append("Binay audit researcher identity mismatch")
if avishek_audit.get("classification")!="FIRST_DRAFT_SOURCE_INTAKE__ARCHIVED_CONVERSION_REFERENCE__NO_PROMOTED_ACTIVE_THESIS_AUTHORITY":
    errors.append("Avishek active-authority scope drift")
if root_rescan.get("current_inventory_count")!=len(root_rescan.get("children",[])):
    errors.append("02_Thesis rescan child-count mismatch")
if not any(x.get("name")=="Thesis_Safal_Dawadi_Rework_CM" and x.get("position")==11 for x in root_rescan.get("children",[])):
    errors.append("newly observed Safal Dawadi child missing from rescan")
if not any(d.get("debt_id")=="DEBT-AVISHEK-001" and d.get("status")=="HOLD" for d in debt_rows):
    errors.append("Avishek source-intake hold missing")
for slug,audit in audit_batch.items():
    if not audit.get("audit_id") or not audit.get("root_folder_id"): errors.append(f"{slug}: audit identity incomplete")
    if not any(d.get("audit_slug")==slug or audit.get("researcher_id") and d.get("researcher_id")==audit.get("researcher_id") for d in debt_rows):
        errors.append(f"{slug}: no traceable debt/hold")
if audit_batch["safal-dawadi"].get("registered_researcher") is not True:
    errors.append("Safal Dawadi independent admission missing")
if not any(d.get("debt_id")=="DEBT-MANOJ-001" and d.get("status")=="HOLD" for d in debt_rows):
    errors.append("Manoj thesis-authority HOLD missing")
if not any(d.get("debt_id")=="DEBT-OPS-PAGES-001" and d.get("status")=="CLOSED" for d in debt_rows):
    errors.append("resolved Pages deployment readback missing")
if policy.get("repository_role")!="R_AND_D_CODE_POINTER_AND_CONTROL_PORTAL": errors.append("repository policy role mismatch")
# Main/lane binary guard. Git history may contain binaries; current tree may not.
try:
    files=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
except Exception:
    files=[str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()]
forbidden={".pdf",".pptx",".docx",".xlsx",".xls",".png",".jpg",".jpeg",".gif",".webp",".zip",".7z",".rar",".glb",".obj",".ifc",".dwg",".dxf"}
bad=[f for f in files if Path(f).suffix.lower() in forbidden]
if bad: errors.append("binary/artifact files forbidden in current tree: "+", ".join(bad[:20]))
for f in files:
    if re.search(r"(^|/)(node_modules|dist|out|\.next)/",f): errors.append(f"generated directory committed: {f}")
ap=argparse.ArgumentParser(); ap.add_argument("--site"); args=ap.parse_args()
if args.site:
    site=ROOT/args.site
    expected=["index.html","roadmap/index.html","branches/index.html","assets/theme.js","assets/branches.js","researchers/index.html","workspace/index.html","how-to/index.html","controls/index.html","debts/index.html"]
    expected += [f"researchers/{r['slug']}/index.html" for r in rows]
    expected += [f"controls/{x}/index.html" for x in ("discussion","latex","presentation","website")]
    expected += ["controls/latex/safal-dawadi/index.html"]
    debt_researcher_ids={d.get("researcher_id") for d in debt_rows if d.get("status") in ("OPEN","HOLD") and d.get("researcher_id")}
    expected += [f"researchers/{r['slug']}/debts/index.html" for r in rows if r.get("researcher_id") in debt_researcher_ids]
    expected += ["audits/02-thesis/index.html","audits/02-thesis/manoj-bhandari/index.html","audits/02-thesis/manoj-bhandari/debts/index.html","audits/02-thesis/avishek-kumar-mandal/index.html","audits/02-thesis/avishek-kumar-mandal/debts/index.html"]
    expected += [f"audits/02-thesis/{slug}/{suffix}" for slug in audit_batch_slugs for suffix in ("index.html","debts/index.html")]
    expected += ["researchers/fabin-gurung/websites/aec/index.html","researchers/fabin-gurung/websites/hydropower-phd/index.html","researchers/fabin-gurung/websites/hydropower-phd/proposal-defense/index.html","methodology-demo/index.html","hydropower-data-model/model.json","hydropower-data-schema/index.html","hydropower-data-tables/index.html","hydropower-data-graph/index.html","hydropower-nepal-map/index.html"]
    expected += ["aec/index.html","hydropower/index.html","hydropower/proposal-defense/index.html"]
    for rel in expected:
        if not (site/rel).is_file(): errors.append(f"site missing {rel}")
# Shared LaTeX v1.2.0 public-safe governance package
required_latex=[
    "controls/latex/README.md","controls/latex/pu-format-parity-audit.json","controls/latex/format-authorities.json",
    "controls/latex/pu-msc-format.rules.json","controls/latex/build-contract.json",
    "controls/latex/qa-contract.json","controls/latex/release-contract.json",
    "controls/latex/migration-status.json","schemas/latex-project.schema.json",
    "researchers/safal-dawadi/latex/README.md",
    "researchers/safal-dawadi/latex/control.json",
    "researchers/safal-dawadi/latex/source-baseline.json",
    "docs/LATEX_GOVERNANCE_PRE_AND_SCOPE_20261009.md"
]
for p in required_latex:
    if not (ROOT/p).is_file(): errors.append(f"required LaTeX bridge missing: {p}")
    elif p.endswith(".json"): load(p)
if latex_policy.get("control_id")!="RD-CONTROL-LATEX-001" or latex_policy.get("control_version")!="2.1.0":
    errors.append("LaTeX control identity/version failed")
if latex_policy.get("shared_package")!="controls/latex/":
    errors.append("shared LaTeX inheritance path failed")
fmt=load("controls/latex/format-authorities.json")
rul=load("controls/latex/pu-msc-format.rules.json")
mig=load("controls/latex/migration-status.json")
scoped=load("researchers/safal-dawadi/latex/control.json")
baseline=load("researchers/safal-dawadi/latex/source-baseline.json")
if not any(x.get("id")=="1FjbNdNN_Fb_tKoapaYHW2jLoEF9lqxrYPYrCwTi87Ys" for x in fmt.get("sources",[])):
    errors.append("PU v1.13 authority not referenced")
if not any(x.get("id")=="1jc6WIqXbAixAYYndeB2Idw59fAzjBbnDKlq49THeu_A" for x in fmt.get("sources",[])):
    errors.append("thesis-wide authority not referenced")
if rul.get("discovered_unique_rule_ids")!=len({x.get("id") for x in rul.get("rule_index",[])}):
    errors.append("PU rule index count/uniqueness wrong")
if not {"PU-FMT-087","PU-FMT-097","PU-FMT-143"} <= {x.get("id") for x in rul.get("rule_index",[])}:
    errors.append("key PU migration/overfull/immutable rule IDs missing")
parity=load("controls/latex/pu-format-parity-audit.json")
audit_ids=[x.get("id") for x in parity.get("per_rule",[])]
if len(audit_ids)!=144 or len(set(audit_ids))!=144 or set(audit_ids)!={x.get("id") for x in rul.get("rule_index",[])}:
    errors.append("PU 144-source-rule parity audit incomplete or mismatched")
if parity.get("absent_from_source")!=["PU-FMT-076"] or parity.get("counts",{}).get("full_production_verified")!=0:
    errors.append("PU missing source number/production QA gate misrepresented")
if any(x.get("actual_compiled_pdf_verified") is not False or not x.get("approved_rule") or not x.get("title") for x in parity.get("per_rule",[])):
    errors.append("PU rule source mapping or QA hold metadata incomplete")
if mig.get("cutover")!="NOT_APPROVED" or mig.get("format_rule_ids_full_automated_enforcement")!=0:
    errors.append("unearned PU parity promotion")
if scoped.get("researcher_id")!="RSH-010" or scoped.get("shared_control")!="controls/latex/tower.json":
    errors.append("Safal inheritance identity/control mismatch")
if scoped.get("scientific_approval")!="HOLD" or scoped.get("release_ready") is not False:
    errors.append("Safal scientific approval and release must remain HOLD")
git_source_admitted=(scoped.get("source_admission")=="VERIFIED")
if scoped.get("source_admission") not in ("HOLD","VERIFIED"):
    errors.append("Safal source admission state must be explicit HOLD or VERIFIED")
if git_source_admitted:
    expected_hash="9c7bb25b84bd4a85aea85f137fdd8d080ab85c8fa18622a6d1ad9386d8f585bd"
    selected=baseline.get("selected_baseline") or {}
    if selected.get("artifact_sha256")!=expected_hash or selected.get("drive_source_zip_id")!="1mgJ-_-Jc-z4XionxbjfpD9zinynSor9c":
        errors.append("Safal verified source admission lacks exact seq15 source authority/hash")
    if baseline.get("source_git_admission")!="VERIFIED" or baseline.get("selected_target",{}).get("bytes_rehashed") is not True:
        errors.append("Safal source admission cannot bypass byte verification")
    if safal_policy.get("gates",{}).get("source_reconciliation")!="VERIFIED" or safal_policy.get("gates",{}).get("public_git_clearance")!="VERIFIED" or safal_policy.get("gates",{}).get("source_admission")!="VERIFIED":
        errors.append("Safal verified Git admission lacks three explicit source gates")
    root=ROOT/"researchers/safal-dawadi/latex/manuscript"
    for rel in ("main.tex","08_reference.bib","chapters/chapter4_results_discussion.tex","safal_pages.tex","safal_dependencies.tex"):
        if not (root/rel).is_file(): errors.append("Safal verified source file missing: "+rel)
    for bad in ("pu_fst_final_report.sty","private_fonts/times.ttf","PokharaUniversity.jpg","main.pdf"):
        if (root/bad).exists(): errors.append("Safal restricted or competing format asset in public Git: "+bad)
if scoped.get("citation_style") not in ("APA7","IEEE","HARVARD","UNKNOWN"):
    errors.append("invalid project-specific bibliography style")
if scoped.get("document_stage") not in ("PROPOSAL","MIDTERM","FINAL_THESIS","DEFENSE","UNKNOWN"):
    errors.append("invalid or inherited document stage")
if not git_source_admitted and (baseline.get("selected_baseline") is not None or baseline.get("source_git_admission")!="HOLD"):
    errors.append("Safal source incorrectly promoted before gate verification")
if scoped.get("document_stage")!="FINAL_THESIS" or scoped.get("current_manifest_candidate",{}).get("version")!="v1.2":
    errors.append("Safal final-report identity or v1.2 Midterm predecessor pointer lost")
if git_source_admitted and scoped.get("selected_manuscript_target")!="V1.9_LOCAL_SEQ15_SOURCE_SHA256_VERIFIED__PDF_NOT_RECONCILED":
    errors.append("Safal admitted Git source must refer to exact v1.9 hash, leaving PDF unresolved")
if not git_source_admitted and scoped.get("selected_manuscript_target")!="V1.9_LOCAL_SEQ15_Q1_B_BYTE_MIRROR_PENDING":
    errors.append("Safal held source must preserve its originally reported v1.9 target")
if baseline.get("latest_manifest_designated_candidate",{}).get("classification")!="CURRENT_CONTROLLED_PREVIEW_NON_PRODUCTION":
    errors.append("Safal October 2026 nonproduction preview state lost")
if baseline.get("a9_main_registry_observed",{}).get("safal_row_consumed_cursor")!=2:
    errors.append("Do not claim main library seq15 ACK; main registry historic row is seq2")
if not any(x.get("researcher_id")=="RSH-004" and x.get("slug")=="safal-thapa" for x in rows):
    errors.append("Safal Thapa identity must remain distinct RSH-004")
if args.site:
    for route in ("controls/latex/index.html","researchers/safal-dawadi/latex/index.html"):
        if not (ROOT/args.site/route).is_file(): errors.append(f"site missing LaTeX route {route}")
    for term in ("Source files","Original authorities","Format selection","Full PU formatting source-parity audit","Approved Q1B / Q2A / Q3A"):
        try:
            if term not in (ROOT/args.site/"controls/latex/index.html").read_text(encoding="utf-8"):
                errors.append(f"latex portal missing section {term}")
        except FileNotFoundError: pass

# Single canonical shared-template and per-researcher extension validation
import ast, sys
# Reusable A9 thesis folder contract and PU route machine-validation.
for command in (
    [sys.executable,str(ROOT/"scripts/researchers/normalize.py"),"--validate"],
    [sys.executable,str(ROOT/"scripts/researchers/test_normalization.py")],
    [sys.executable,str(ROOT/"scripts/latex/universal_preflight.py"),"--policy-check"],
):
    p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
    if p.returncode:
        errors.append("thesis infrastructure regression failed "+command[1]+": "+(p.stdout+p.stderr)[-1500:])
for command in (
    [sys.executable,str(ROOT/"scripts/latex/universal_compile.py"),"--help"],
    [sys.executable,str(ROOT/"scripts/latex/pdf_technical_qa.py"),"--help"],
):
    p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
    if p.returncode:
        errors.append("universal Linux build command interface failed "+command[1]+": "+(p.stdout+p.stderr)[-500:])
if args.site:
    for required_route in ("thesis-infrastructure/index.html","data/researcher-folder-roles.json","data/latex-build-profiles.json"):
        if not (ROOT/args.site/required_route).is_file():
            errors.append("thesis infrastructure website route/data missing: "+required_route)
# Owner-only migration controls: prompt existence is NOT a Drive mutation.
owner=load("controls/researcher-migration-rules.json")
status_registry=load("registry/researcher-migration-status.json")
if owner.get("trigger")!="USER_PASTES_EXACT_RESEARCHER_PROMPT_IN_OWNING_RESEARCHER_CHAT":
    errors.append("Owner-only execution trigger was weakened")
if len(status_registry.get("records",[]))!=11:
    errors.append("Missing one or more owner migration records")
for record in status_registry.get("records",[]):
    if record.get("user_trigger_observed") or record.get("drive_deletes")!=0 or record.get("main_ack")!="NOT_ATTEMPTED":
        errors.append("Unsafe or falsely executed migration status "+str(record.get("researcher_id")))
    prompt=record.get("prompt_path","")
    if not prompt.startswith("prompts/researchers/") or not (ROOT/prompt).is_file():
        errors.append("Missing opt-in researcher prompt "+prompt)
owner_check=subprocess.run([sys.executable,str(ROOT/"scripts/researchers/generate_prompts.py"),"--check"],cwd=ROOT,text=True,capture_output=True)
if owner_check.returncode:
    errors.append("11 generated researcher prompts are out of sync: "+(owner_check.stdout+owner_check.stderr)[-1800:])
# Public prompt browser must remain a copy-only frontend, never an execution backend.
if args.site:
    entry=ROOT/args.site/"owner-prompts/index.html"
    if not entry.is_file():
        errors.append("Owner prompt reading desk index missing")
    for row in status_registry.get("records",[]):
        path=ROOT/args.site/"owner-prompts"/row["slug"]/"index.html"
        if not path.is_file():
            errors.append("Owner prompt page absent "+row["researcher_id"])
            continue
        txt=path.read_text(encoding="utf-8")
        for marker in ("data-copy-owner-prompt","readonly","NO DELETE"):
            if marker not in txt:
                errors.append("Owner prompt page lacks safeguard "+row["researcher_id"]+" "+marker)
    if not (ROOT/args.site/"assets/prompt-copy.js").is_file():
        errors.append("Owner prompt copy script was not deployed")
# Public discovery catalogue must remain a non-authoritative index of existing public-safe metadata.
catalogue_test=subprocess.run([sys.executable,str(ROOT/"scripts/test_site_search.py")],cwd=ROOT,text=True,capture_output=True)
if catalogue_test.returncode:
    errors.append("research catalogue regression failed: "+(catalogue_test.stdout+catalogue_test.stderr)[-2500:])
if args.site:
    search_page=ROOT/args.site/"search/index.html"
    search_index=ROOT/args.site/"data/research-index.json"
    if not search_page.is_file() or not search_index.is_file():
        errors.append("R&D research search page/data missing")
    else:
        data=json.loads(search_index.read_text(encoding="utf-8"))
        if len(data.get("entries",[]))<100:
            errors.append("R&D research search index unexpectedly thin")
        if "research-search" not in search_page.read_text(encoding="utf-8"):
            errors.append("R&D search control absent")
if args.site:
    index=ROOT/args.site/"index.html"
    thesis=ROOT/args.site/"thesis-infrastructure/index.html"
    if index.is_file():
        homepage=index.read_text(encoding="utf-8")
        for text_needed in ("data-winged-book","data-motion-toggle","Where curiosity","assets/motion.js"):
            if text_needed not in homepage:
                errors.append("Living library hero missing "+text_needed)
    if thesis.is_file():
        page=thesis.read_text(encoding="utf-8")
        for item in status_registry["records"]:
            if item["prompt_path"].split("/")[-1] not in page:
                errors.append("Researcher owner prompt absent from thesis portal: "+item["researcher_id"])
for path in ("web/living-hero.html","web/motion.js","web/prompt-copy.js","web/styles.css","prompts/researcher_owner_execution_master.md","scripts/researchers/generate_prompts.py","schemas/researcher-migration-status.schema.json","controls/website-living-library.json"):
    if not (ROOT/path).is_file(): errors.append("theme or owner prompt file missing: "+path)
# Syntax and executable HOLD/PRESENT source-gate regression: green CI must NOT be construed as PDF certified.
for script in ("scripts/latex/safal_build.py","scripts/latex/validate_shared.py","scripts/build_site.py","scripts/validate_site_links.py","scripts/test_site_links.py","scripts/site_core.py","scripts/site_pages.py","scripts/site_search.py","scripts/test_site_search.py","scripts/researchers/normalize.py","scripts/researchers/test_normalization.py","scripts/researchers/generate_prompts.py","scripts/latex/universal_preflight.py","scripts/latex/universal_compile.py","scripts/latex/pdf_technical_qa.py"):
    try:
        ast.parse((ROOT/script).read_text(encoding="utf-8"),filename=script)
    except (SyntaxError,OSError) as e:
        errors.append("Python script syntax/read failed "+script+": "+str(e))
source_check=subprocess.run([sys.executable,str(ROOT/"scripts/latex/safal_build.py"),"--mode","check"],cwd=ROOT,text=True,capture_output=True)
if source_check.returncode!=0 or not any(token in source_check.stdout for token in ("SOURCE_GATE=HOLD_NOT_ADMITTED","SOURCE_GATE=SOURCE_PRESENT")):
    errors.append("Safal build source-check not executable or missing explicit HOLD/PRESENT label: "+(source_check.stdout+source_check.stderr)[:500])
shared_test=subprocess.run([sys.executable,str(ROOT/"scripts/latex/validate_shared.py")],cwd=ROOT,text=True,capture_output=True)
if shared_test.returncode!=0:
    errors.append("shared template inheritance check failed: "+(shared_test.stdout+shared_test.stderr).strip()[:3000])
# Portal reliability: run unit tests even without a generated site.
unit=subprocess.run([sys.executable,str(ROOT/"scripts/test_site_links.py")],cwd=ROOT,text=True,capture_output=True)
if unit.returncode!=0:
    errors.append("portal link checker unit tests FAILED: "+(unit.stdout+unit.stderr)[-2000:])
if args.site:
    link_test=subprocess.run(
        [sys.executable,str(ROOT/"scripts/validate_site_links.py"),"--site",args.site],
        cwd=ROOT,text=True,capture_output=True
    )
    if link_test.returncode!=0:
        errors.append("broken generated-site navigation/assets: "+(link_test.stdout+link_test.stderr)[-6200:])
if args.site:
    single_page=ROOT/args.site/"controls/latex/index.html"
    if single_page.exists() and "One template for every researcher" not in single_page.read_text(encoding="utf-8"):
        errors.append("canonical shared LaTeX website section missing")
if errors:
    print("JP R&D VALIDATION: FAIL")
    for e in errors: print("- "+e)
    raise SystemExit(1)
print(f"JP R&D VALIDATION: PASS researchers={len(rows)} lanes={len(lane_names)} websites={len(website_rows)} debts={len(debt_rows)} legacy={len(branches.get('archived_legacy',[]))}")
