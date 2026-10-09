#!/usr/bin/env python3
"""Append a proposal to the sole R&D LaTeX amendment register.
Run locally, inspect the diff, and commit through the governed Git workflow.
Scientific approval, central template promotion and Drive writes are NOT automatic.
"""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REGISTER=ROOT/"controls/latex/change-register.json"
RESEARCHERS=ROOT/"registry/researchers.json"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--researcher-id",required=True)
    p.add_argument("--classification",choices=["GLOBAL_CANDIDATE","RESEARCHER_ONLY"],required=True)
    p.add_argument("--summary",required=True)
    p.add_argument("--source",required=True,help="Affected researcher source/path or output/source manifest")
    p.add_argument("--evidence",required=True,help="Stable Drive evidence ID or approved public link")
    p.add_argument("--pu-rule",default="",help="Optional original PU-FMT rule ID")
    args=p.parse_args()
    if not args.summary.strip() or len(args.summary.strip())<10:
        p.error("Explain the formatting defect or proposed improvement (at least 10 chars)")
    if not args.evidence.strip(): p.error("evidence pointer cannot be blank")
    rs=json.loads(RESEARCHERS.read_text(encoding="utf-8"))["researchers"]
    if args.researcher_id not in {r["researcher_id"] for r in rs}:
        p.error("researcher is not registered")
    if args.pu_rule and not re.fullmatch(r"PU-FMT-\d{3}",args.pu_rule):
        p.error("PU rule must be PU-FMT-NNN")
    reg=json.loads(REGISTER.read_text(encoding="utf-8"))
    num=reg["next_number"]
    assert num>=101
    item={
        "change_id":f"RD-LTX-CHG-{num:03d}",
        "researcher_id":args.researcher_id,
        "classification":args.classification,
        "summary":args.summary.strip(),
        "source_paths":[args.source],
        "before_after_qa_evidence":args.evidence.strip(),
        "pu_rule_references":[args.pu_rule] if args.pu_rule else [],
        "disposition":"PROPOSED",
        "target_shared_rule":None,
        "git_commit_sha_after_merge":None,
        "scoped_extension_path":None
    }
    reg["entries"].append(item)
    reg["next_number"]=num+1
    tmp=REGISTER.with_name(REGISTER.name+".tmp")
    tmp.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    tmp.replace(REGISTER)
    print(item["change_id"]+": proposed in central register; review before changing shared template or adding exception")
if __name__=="__main__":main()
