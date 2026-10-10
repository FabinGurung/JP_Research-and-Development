#!/usr/bin/env python3
"""DRAFT-only enterprise template renderer. Private inputs stay outside Git."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TOKEN=re.compile(r"\{\{([a-z_]+)\}\}")
ESC={"&":r"\&","%":r"\%","$":r"\$","#":r"\#","_":r"\_","{":r"\{","}":r"\}","\\":r"\textbackslash{}"}
def escape(value):
    if not isinstance(value,str) or not value.strip(): raise ValueError("Missing text")
    return "".join(ESC.get(c,c) for c in value)
def render(document):
    kind=document["template_id"]
    if not re.fullmatch("[a-z-]+",kind):raise ValueError("Invalid document type")
    config=json.loads((ROOT/"controls/document-engineering/types"/(kind+".json")).read_text())
    fields=document["fields"]
    if set(fields)!=set(config["required_fields"]): raise ValueError("Required fields mismatch")
    source=(ROOT/"templates/enterprise/v2"/(kind+".tex")).read_text()
    if set(TOKEN.findall(source))!=set(fields): raise ValueError("Template/schema mismatch")
    output=TOKEN.sub(lambda match:escape(fields[match.group(1)]),source)
    return output,{"state":"DRAFT_NOT_SIGNABLE","release":"HOLD_HUMAN_REVIEW","type_id":kind}
