from __future__ import annotations
import hashlib, json, re
from pathlib import Path

class ValidationError(Exception):
    pass

def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip().lower()

def _resolve_asset(base: Path, p):
    if not p:
        return None
    q=Path(str(p))
    return q if q.is_absolute() else (base/q).resolve()

def validate_content(content: dict, theme: dict, base_dir: str | Path) -> dict:
    errors, warnings = [], []
    base = Path(base_dir)
    if not isinstance(content, dict):
        errors.append("content must be an object")
        return {"ok": False, "errors": errors, "warnings": warnings}
    meta = content.get("metadata") or {}
    slides = content.get("slides")
    if not meta.get("title"):
        errors.append("metadata.title is required")
    if not meta.get("researcher"):
        errors.append("metadata.researcher is required")
    if not isinstance(slides, list) or not slides:
        errors.append("slides must be a non-empty array")
        return {"ok": False, "errors": errors, "warnings": warnings}

    # v2.2 title-branding hard gate: default/minimum is 2.25 in, i.e. >2x the former 1.00 in project baseline.
    branding=theme.get("branding") or {}
    if branding.get("title_logo_required", True):
        logo=_resolve_asset(base, meta.get("logo"))
        if not logo or not logo.exists():
            errors.append("metadata.logo is required and must resolve to an existing canonical institutional-logo file")
        else:
            actual=sha256_file(logo)
            supplied=str(meta.get("logo_sha256") or "").lower()
            required=str(branding.get("canonical_logo_sha256") or "").lower()
            if supplied and actual.lower()!=supplied:
                errors.append("metadata.logo_sha256 does not match the supplied logo file")
            if required and actual.lower()!=required:
                errors.append("title logo is not the canonical governed institutional logo SHA-256")
        min_logo=float(branding.get("title_logo_min_in", 2.25))
        size=float(meta.get("title_logo_size_in", branding.get("title_logo_default_in", min_logo)))
        if size < min_logo:
            errors.append(f"metadata.title_logo_size_in={size:.3f} is below governed minimum {min_logo:.3f} in")

    # v2.2 supervisor metadata hard gate. Do not invent: availability is resolved from the project authority.
    sup_available=meta.get("supervisor_available", True)
    supervisor=meta.get("supervisor") or {}
    if sup_available and not str(supervisor.get("name","")).strip():
        errors.append("verified/available supervisor name is mandatory on the title slide")
    cos=meta.get("co_supervisors") or []
    if not isinstance(cos,list):
        errors.append("metadata.co_supervisors must be an array")
        cos=[]
    co_available=bool(meta.get("co_supervisors_available", bool(cos)))
    if co_available and not cos:
        errors.append("co-/sub-supervisor metadata is marked available but no names were supplied")
    for j,obj in enumerate(cos,1):
        if not isinstance(obj,dict) or not str(obj.get("name","")).strip():
            errors.append(f"co-/sub-supervisor {j}: name is required when the role is available")

    forbidden = [x.lower() for x in theme["rules"].get("client_forbidden_terms", [])]
    client = bool(meta.get("client_facing", True))
    max_title = int(theme["rules"].get("max_title_chars", 90))
    max_bullets = int(theme["rules"].get("max_text_only_bullets", 5))
    max_bullet_chars = int(theme["rules"].get("max_bullet_chars", 180))

    for i, slide in enumerate(slides, 1):
        stype = slide.get("type")
        if stype not in {"title","bullets","section","figure","two_figures","closing","literature_table","methodology_flow"}:
            errors.append(f"slide {i}: unsupported type {stype!r}")
            continue
        title = str(slide.get("title",""))
        if stype != "title" and not title:
            errors.append(f"slide {i}: title is required")
        if len(title) > max_title:
            warnings.append(f"slide {i}: title length {len(title)} exceeds {max_title}; shorten before production")

        bullets = slide.get("bullets") or []
        if stype == "bullets":
            if not bullets:
                errors.append(f"slide {i}: bullets slide requires bullets")
            if len(bullets) > max_bullets:
                errors.append(f"slide {i}: {len(bullets)} bullets exceeds governed default {max_bullets}; split slide")
            for j, b in enumerate(bullets, 1):
                if len(str(b)) > max_bullet_chars:
                    errors.append(f"slide {i} bullet {j}: exceeds {max_bullet_chars} chars; shorten/split")
        visible_text = " ".join([title, str(slide.get("subtitle","")), str(slide.get("caption",""))] + [str(x) for x in bullets])
        if client:
            norm = _norm(visible_text)
            for term in forbidden:
                if term and term in norm:
                    errors.append(f"slide {i}: client-facing forbidden term detected: {term}")

        def check_asset(obj, label):
            if not obj: return
            p = obj.get("path")
            if not p:
                errors.append(f"slide {i} {label}: missing path")
                return
            path = _resolve_asset(base,p)
            if not path.exists():
                errors.append(f"slide {i} {label}: asset not found: {path}")
                return
            expected = obj.get("sha256")
            if expected:
                actual = sha256_file(path)
                if actual.lower() != str(expected).lower():
                    errors.append(f"slide {i} {label}: SHA-256 mismatch")
        if stype == "figure":
            check_asset(slide.get("figure"), "figure")
        elif stype == "two_figures":
            figs = slide.get("figures") or []
            if len(figs) != 2:
                errors.append(f"slide {i}: two_figures requires exactly 2 figures")
            for j, obj in enumerate(figs, 1):
                check_asset(obj, f"figure{j}")
    # The literature-specific semantic gate runs independently with the current evidence map.
    # Basic structural failures must still be detected on fixture builds.
    from a9_literature_table import validate_literature
    lit_structure = validate_literature(content, None, fixture=True)
    errors.extend(lit_structure["errors"])
    warnings.extend(lit_structure["warnings"])
    from a9_methodology_flow import validate_methodology
    method_structure = validate_methodology(content, None, fixture=True)
    errors.extend(method_structure["errors"])
    warnings.extend(method_structure["warnings"])
    return {"ok": not errors, "errors": errors, "warnings": warnings}
