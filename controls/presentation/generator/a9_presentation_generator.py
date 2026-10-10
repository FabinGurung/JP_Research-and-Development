from __future__ import annotations
import json, os, math
from pathlib import Path
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from PIL import Image

PT_PER_IN = 72.0

def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def _fc_match(family):
    try:
        cp=subprocess.run(["fc-match","-f","%{family}\n%{file}\n",family],capture_output=True,text=True,check=True)
        lines=[x.strip() for x in cp.stdout.splitlines() if x.strip()]
        return (lines[0] if lines else "", lines[1] if len(lines)>1 else "")
    except Exception:
        return ("","")

def _requested_font(theme, production=False):
    return theme["fonts"]["production_family"] if production else theme["fonts"]["preview_family"]

def _pdf_font(theme, production=False):
    requested = _requested_font(theme, production)
    fam, path = _fc_match(requested)
    if production and requested.lower() not in fam.lower():
        raise RuntimeError(f"Production font gate failed: exact {requested!r} not available; fc-match returned {fam!r}")
    if path and Path(path).exists():
        internal = "A9_PROD_FONT" if production else "A9_PREVIEW_FONT"
        if internal not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(internal, path))
        return internal
    if production:
        raise RuntimeError(f"Production font gate failed: no TTF file resolved for {requested!r}")
    return "Times-Roman"

def _pptx_font(theme, production=False):
    requested = _requested_font(theme, production)
    fam, _path = _fc_match(requested)
    if production and requested.lower() not in fam.lower():
        raise RuntimeError(f"Production font gate failed: exact {requested!r} not available; fc-match returned {fam!r}")
    return requested

def _wrap_text(text, font_name, font_size, max_width_pt, pdf=True):
    words = str(text).split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        cand = cur + " " + w
        width = stringWidth(cand, font_name, font_size) if pdf else len(cand)*font_size*0.48
        if width <= max_width_pt:
            cur = cand
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def _fit_image(path, box_w_in, box_h_in):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(box_w_in/iw, box_h_in/ih)
    return iw*scale, ih*scale

def _asset_path(p):
    if not p:
        return None
    q = Path(str(p))
    return q if q.is_absolute() else Path.cwd() / q

def _supervisor_lines(meta):
    lines=[]
    sup=meta.get("supervisor") or {}
    if str(sup.get("name","")).strip():
        label="Supervisor"
        text=f"{label}: {sup['name']}"
        if str(sup.get("designation","")).strip(): text += f" — {sup['designation']}"
        lines.append(text)
    for obj in (meta.get("co_supervisors") or []):
        role=str(obj.get("role") or "Co-Supervisor").strip()
        name=str(obj.get("name") or "").strip()
        if not name: continue
        text=f"{role}: {name}"
        if str(obj.get("designation","")).strip(): text += f" — {obj['designation']}"
        lines.append(text)
    return lines

def _lit_columns(slide):
    """The layout is general-purpose; the words are taken from verified source data."""
    if slide.get("columns", 3) == 4:
        return ["Author (Year)", "Key Finding", "Method / Limitation", "Relevance to This Study"], [1.60, 2.75, 1.95, 2.80], ["author_year", "key_finding", "method_or_limitation", "project_relevance"]
    return ["Author (Year)", "Key Finding", "Relevance to This Study"], [1.95, 3.50, 3.65], ["author_year", "key_finding", "project_relevance"]


def _pdf_literature_table(c, slide, font, left, W, H, top, bottom, title_pt):
    from reportlab.lib.colors import HexColor
    headers, widths_in, fields = _lit_columns(slide)
    title = slide.get("title", "Literature Review")
    c.setFillColor(HexColor("#000000")); c.setFont(font, title_pt)
    c.drawString(left, H-top-title_pt, title)
    y = H-top-title_pt-43
    header_h = 47
    x = left
    c.setFillColor(HexColor("#EDEDED"))
    c.rect(left, y-header_h, sum(widths_in)*72, header_h, fill=1, stroke=0)
    c.setFillColor(HexColor("#000000"))
    for label,w in zip(headers,widths_in):
        c.setFont(font, 13)
        c.drawString(x+9,y-28,label)
        x+=w*72
    y-=header_h
    rows=slide.get("rows",[])
    if not rows: raise ValueError("empty literature matrix")
    row_h=min(123, (y-bottom-34)/len(rows))
    if row_h < 94: raise ValueError("literature table row overflow: paginate earlier")
    for row in rows:
        x=left
        for field,w in zip(fields,widths_in):
            val=str(row.get(field, ""))
            point=13.3 if field in {"key_finding","project_relevance"} else 12.5
            lines=_wrap_text(val,font,point,w*72-19)
            if len(lines)*(point*1.23)>row_h-15:
                raise ValueError(f"literature table cell too long: {field}: {val[:60]}")
            c.setFont(font,point)
            for k,line in enumerate(lines):
                c.drawString(x+9,y-18-k*point*1.23,line)
            x+=w*72
        c.setStrokeColor(HexColor("#B5B5B5"))
        c.line(left,y-row_h,left+sum(widths_in)*72,y-row_h)
        y-=row_h
    x=left
    for w in [0,*widths_in]:
        if w: x+=w*72
        c.line(x, H-top-title_pt-43, x,y)
    c.setStrokeColor(HexColor("#000000"))
    c.setFont(font,10)
    c.drawString(left,bottom+10,"Full references are provided in the thesis bibliography.")


def _pptx_literature_table(slide, spec, font, left, top, title_pt):
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_ANCHOR
    headers,widths,fields=_lit_columns(spec)
    _add_textbox(slide,left,top,9.1,0.58,spec.get("title","Literature Review"),title_pt,font)
    rows=spec.get("rows",[])
    table_h=0.59+1.60*len(rows)
    tbl_shape=slide.shapes.add_table(len(rows)+1,len(headers), Inches(left), Inches(1.18), Inches(sum(widths)), Inches(table_h))
    table=tbl_shape.table
    for j,w in enumerate(widths): table.columns[j].width=Inches(w)
    table.rows[0].height=Inches(0.59)
    for ri in range(1,len(rows)+1): table.rows[ri].height=Inches(1.60)
    for ri in range(len(rows)+1):
        for ci,field in enumerate(fields):
            cell=table.cell(ri,ci)
            cell.margin_left=Inches(0.12);cell.margin_right=Inches(0.10)
            cell.margin_top=Inches(0.10);cell.margin_bottom=Inches(0.09)
            cell.vertical_anchor=MSO_ANCHOR.TOP
            cell.text=headers[ci] if ri==0 else str(rows[ri-1].get(field,""))
            cell.fill.solid()
            cell.fill.fore_color.rgb=RGBColor(237,237,237) if ri==0 else RGBColor(255,255,255)
            # Native PowerPoint cells remain editable; unobtrusive rules aid scanning.
            from pptx.oxml.xmlchemy import OxmlElement
            from pptx.oxml.ns import qn
            tcpr = cell._tc.get_or_add_tcPr()
            for edge in ("lnB", "lnR"):
                tag = qn("a:" + edge)
                if tcpr.find(tag) is None:
                    line = OxmlElement("a:" + edge)
                    line.set("w", "6500")
                    fill = OxmlElement("a:solidFill")
                    srgb = OxmlElement("a:srgbClr")
                    srgb.set("val", "C4C4C4")
                    fill.append(srgb); line.append(fill); tcpr.append(line)
            tf=cell.text_frame; tf.word_wrap=True
            for paragraph in tf.paragraphs:
                paragraph.font.name=font
                paragraph.font.size=Pt(12.5 if ci==0 else 13.3)
                paragraph.font.bold=ri==0
                paragraph.font.color.rgb=RGBColor(0,0,0)
    _add_textbox(slide,left,6.58,9.1,0.24,"Full references are provided in the thesis bibliography.",10,font)


def _method_stage_text(stage):
    return str(stage.get('title','')), str(stage.get('description',''))

def _pdf_methodology_flow(c, slide, font, W, H, left, right, top, title_pt):
    # One semantic row in 4:3 landscape, vector geometry; scientific provenance is a sidecar.
    from reportlab.lib.colors import HexColor
    stages=slide['stages']; count=len(stages)
    if count>6: raise ValueError('methodology must be paginated before rendering')
    c.setFillColor(HexColor('#141414')); c.setFont(font,title_pt)
    c.drawString(left,H-top-title_pt,slide.get('title','Methodology'))
    usable=W-left-right; arrow_width=19 if count>=5 else 25
    box_w=(usable-arrow_width*(count-1))/count
    if box_w<65: raise ValueError('methodology nodes are too narrow')
    h=152; y=H*0.42
    for i,stage in enumerate(stages):
        x=left+i*(box_w+arrow_width)
        c.setFillColor(HexColor('#F5F5F5'));c.setStrokeColor(HexColor('#898989'))
        c.roundRect(x,y,box_w,h,9,stroke=1,fill=1)
        c.setFillColor(HexColor('#303030'));c.setFont(font,11)
        c.drawString(x+8,y+h-17,f'{i+1:02d}')
        label,description=_method_stage_text(stage)
        title_lines=_wrap_text(label,font,11.5,box_w-16)
        if len(title_lines)>3: raise ValueError('methodology title overflow; shorten stage')
        c.setFont(font,11.5)
        ty=y+h-41
        for line in title_lines:
            c.drawString(x+8,ty,line);ty-=14.3
        description_lines=_wrap_text(description,font,9.7,box_w-16)
        if len(description_lines)>6 or ty-14-(len(description_lines)*12)<y+7:
            raise ValueError('methodology description overflow; shorten stage or paginate')
        c.setFont(font,9.7)
        ty-=10
        for line in description_lines:
            c.drawString(x+8,ty,line);ty-=12
        if i<count-1:
            cy=y+h/2
            c.setStrokeColor(HexColor('#303030'));c.setLineWidth(1.4)
            c.line(x+box_w+2,cy,x+box_w+arrow_width-5,cy)
            ax=x+box_w+arrow_width-5
            p=c.beginPath();p.moveTo(ax,cy);p.lineTo(ax-5,cy+3.5);p.lineTo(ax-5,cy-3.5);p.close()
            c.setFillColor(HexColor('#303030'));c.drawPath(p,stroke=0,fill=1)
    c.setFillColor(HexColor('#444444'));c.setFont(font,10)
    c.drawString(left,72,'Method sequence from the current thesis; evidence/verification details remain in the research record.')

def _pptx_methodology_flow(slide, spec, font, left, top, title_pt):
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    stages=spec['stages'];n=len(stages)
    if n>6: raise ValueError('methodology must be paginated before rendering')
    _add_textbox(slide,left,top,9.1,0.6,spec.get('title','Methodology'),title_pt,font)
    usable=9.1;gap=0.25 if n>=5 else 0.34
    bw=(usable-(n-1)*gap)/n
    if bw < 0.9: raise ValueError('methodology node width insufficient')
    y=2.55;h=2.10
    for i, stage in enumerate(stages):
        x=left+i*(bw+gap)
        shape=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(bw),Inches(h))
        shape.fill.solid();shape.fill.fore_color.rgb=RGBColor(245,245,245)
        shape.line.color.rgb=RGBColor(135,135,135)
        tf=shape.text_frame;tf.clear();tf.word_wrap=True
        tf.margin_left=Inches(0.09);tf.margin_right=Inches(0.07)
        tf.margin_top=Inches(0.11);tf.margin_bottom=Inches(0.08)
        from pptx.enum.text import MSO_ANCHOR
        tf.vertical_anchor=MSO_ANCHOR.TOP
        number=tf.paragraphs[0];number.text=f'{i+1:02d}';number.font.name=font;number.font.size=Pt(10);number.font.color.rgb=RGBColor(35,35,35)
        title_p=tf.add_paragraph();title_p.text=str(stage.get('title',''))
        title_p.font.name=font;title_p.font.size=Pt(11.4);title_p.font.bold=True;title_p.font.color.rgb=RGBColor(20,20,20);title_p.space_before=Pt(9)
        desc_p=tf.add_paragraph();desc_p.text=str(stage.get('description',''))
        desc_p.font.name=font;desc_p.font.size=Pt(9.6);desc_p.font.color.rgb=RGBColor(35,35,35);desc_p.space_before=Pt(7)
        if i<n-1:
            arrow=slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x+bw+0.026), Inches(y+h/2-0.08), Inches(gap-0.05), Inches(0.16))
            arrow.fill.solid();arrow.fill.fore_color.rgb=RGBColor(65,65,65)
            arrow.line.fill.background()
    _add_textbox(slide,left,5.2,9.1,0.4,'Method sequence from the current thesis; full source and verification records remain in the research documentation.',10,font)

def build_pdf(content, theme, out_path, production=False):
    W = theme["canvas"]["width_in"] * PT_PER_IN
    H = theme["canvas"]["height_in"] * PT_PER_IN
    m = theme["safe_margins_in"]
    left, right, top, bottom = [m[k]*PT_PER_IN for k in ("left","right","top","bottom")]
    title_pt = theme["fonts"]["title_pt"]
    body_pt = theme["fonts"]["body_pt"]
    caption_pt = theme["fonts"]["caption_pt"]
    footer_pt = theme["fonts"]["footer_pt"]
    font = _pdf_font(theme, production=production)
    c = pdfcanvas.Canvas(str(out_path), pagesize=(W,H))
    bg = _hex_rgb(theme["colors"]["background"]); fg=_hex_rgb(theme["colors"]["text"])
    slides = content["slides"]; meta=content["metadata"]

    for idx, slide in enumerate(slides, 1):
        c.setFillColorRGB(*(x/255 for x in bg)); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColorRGB(*(x/255 for x in fg)); c.setStrokeColorRGB(*(x/255 for x in fg))
        stype = slide["type"]
        if stype == "title":
            branding=theme.get("branding") or {}
            logo_path = _asset_path(meta.get("logo"))
            logo_size_in = float(meta.get("title_logo_size_in", branding.get("title_logo_default_in", 2.25)))
            if logo_path and logo_path.exists():
                iw, ih = _fit_image(str(logo_path), logo_size_in, logo_size_in)
                logo_h=ih*PT_PER_IN
                c.drawImage(ImageReader(str(logo_path)), (W-iw*PT_PER_IN)/2, H-top-logo_h, iw*PT_PER_IN, logo_h, mask="auto", preserveAspectRatio=True)
                title_start_y = H - top - logo_h - 22
            else:
                title_start_y = H - top - 85
            c.setFont(font, 30)
            y=title_start_y
            for line in _wrap_text(slide.get("title",""), font, 30, W-left-right):
                c.drawCentredString(W/2, y, line); y-=36
            c.setFont(font, 17)
            for line in _wrap_text(slide.get("subtitle",""), font, 17, W-left-right):
                c.drawCentredString(W/2, y-10, line); y-=22
            # Researcher + verified supervisor chain are compulsory title metadata when available.
            meta_lines=[str(meta.get("researcher",""))] + _supervisor_lines(meta) + [str(meta.get("program",""))]
            c.setFont(font, 11)
            y_meta=bottom+96
            for line in meta_lines:
                if line.strip():
                    c.drawCentredString(W/2,y_meta,line); y_meta-=15
        elif stype == "section":
            c.setFont(font, title_pt)
            y=H/2+20
            for line in _wrap_text(slide.get("title",""), font, title_pt, W-left-right):
                c.drawCentredString(W/2,y,line); y-=title_pt*1.25
            c.setFont(font, 16)
            for line in _wrap_text(slide.get("subtitle",""), font, 16, W-left-right):
                c.drawCentredString(W/2,y-10,line); y-=24
        elif stype == "bullets":
            c.setFont(font, title_pt); c.drawString(left,H-top-title_pt,slide.get("title",""))
            y=H-top-title_pt-45
            c.setFont(font, body_pt)
            for b in slide.get("bullets",[]):
                lines=_wrap_text(b,font,body_pt,W-left-right-28)
                c.drawString(left,y,u"\u2022")
                c.drawString(left+24,y,lines[0])
                y-=body_pt*1.35
                for line in lines[1:]:
                    c.drawString(left+24,y,line); y-=body_pt*1.35
                y-=8
        elif stype in {"figure","two_figures"}:
            c.setFont(font,title_pt); c.drawString(left,H-top-title_pt,slide.get("title",""))
            y_top = H-top-title_pt-26
            cap_h = 42
            if stype=="figure":
                obj=slide["figure"]; path=obj["path"]
                box_w=(W-left-right)/PT_PER_IN
                box_h=(y_top-bottom-cap_h)/PT_PER_IN
                iw,ih=_fit_image(path,box_w,box_h)
                x=(W-iw*PT_PER_IN)/2; y=bottom+cap_h+(box_h-ih)*PT_PER_IN/2
                c.drawImage(ImageReader(path),x,y,iw*PT_PER_IN,ih*PT_PER_IN,mask="auto",preserveAspectRatio=True)
            else:
                gap=0.25*PT_PER_IN
                box_w=((W-left-right-gap)/2)/PT_PER_IN
                box_h=(y_top-bottom-cap_h)/PT_PER_IN
                for j,obj in enumerate(slide["figures"]):
                    iw,ih=_fit_image(obj["path"],box_w,box_h)
                    bx=left+j*(box_w*PT_PER_IN+gap)
                    x=bx+(box_w-iw)*PT_PER_IN/2; y=bottom+cap_h+(box_h-ih)*PT_PER_IN/2
                    c.drawImage(ImageReader(obj["path"]),x,y,iw*PT_PER_IN,ih*PT_PER_IN,mask="auto",preserveAspectRatio=True)
            cap=slide.get("caption","")
            if cap:
                c.setFont(font,caption_pt)
                for k,line in enumerate(_wrap_text(cap,font,caption_pt,W-left-right)):
                    c.drawCentredString(W/2,bottom+22-k*caption_pt*1.15,line)
        elif stype == "literature_table":
            _pdf_literature_table(c, slide, font, left, W, H, top, bottom, title_pt)
        elif stype == "methodology_flow":
            _pdf_methodology_flow(c, slide, font, W, H, left, right, top, title_pt)
        elif stype == "closing":
            c.setFont(font, title_pt)
            c.drawCentredString(W/2,H/2+20,slide.get("title",""))
            c.setFont(font,16)
            c.drawCentredString(W/2,H/2-20,slide.get("subtitle",""))
        # footer
        c.setFont(font, footer_pt)
        c.drawString(left, 12, str(meta.get("date","")))
        c.drawCentredString(W/2, 12, str(meta.get("researcher","")))
        c.drawRightString(W-right, 12, f"{idx}/{len(slides)}")
        c.showPage()
    c.save()

def _add_textbox(slide, x,y,w,h,text,size,font,bold=False,align=None):
    sh=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=sh.text_frame; tf.clear(); tf.word_wrap=True; tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    p=tf.paragraphs[0]; p.text=str(text)
    p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor(0,0,0)
    if align is not None: p.alignment=align
    return sh

def build_pptx(content, theme, out_path, production=False):
    prs=Presentation(); prs.slide_width=Inches(theme["canvas"]["width_in"]); prs.slide_height=Inches(theme["canvas"]["height_in"])
    blank=prs.slide_layouts[6]; m=theme["safe_margins_in"]; left=m["left"]; right=m["right"]; top=m["top"]; bottom=m["bottom"]
    font=_pptx_font(theme,production=production); title_pt=theme["fonts"]["title_pt"]; body_pt=theme["fonts"]["body_pt"]; caption_pt=theme["fonts"]["caption_pt"]; footer_pt=theme["fonts"]["footer_pt"]
    slides=content["slides"]; meta=content["metadata"]
    for idx,spec in enumerate(slides,1):
        slide=prs.slides.add_slide(blank)
        stype=spec["type"]
        if stype=="title":
            branding=theme.get("branding") or {}
            logo_path = _asset_path(meta.get("logo"))
            logo_size = float(meta.get("title_logo_size_in", branding.get("title_logo_default_in", 2.25)))
            if logo_path and logo_path.exists():
                with Image.open(logo_path) as im: iw,ih=im.size
                scale=min(logo_size/iw,logo_size/ih); pw,pH=iw*scale,ih*scale
                slide.shapes.add_picture(str(logo_path), Inches((10-pw)/2), Inches(0.30), width=Inches(pw), height=Inches(pH))
                title_y=0.30+pH+0.18
            else:
                title_y=1.45
            _add_textbox(slide,left,title_y,10-left-right,1.86,spec.get("title",""),30,font,bold=False,align=PP_ALIGN.CENTER)
            subtitle_y=title_y+1.88
            _add_textbox(slide,left,subtitle_y,10-left-right,0.55,spec.get("subtitle",""),17,font,align=PP_ALIGN.CENTER)
            meta_y=max(subtitle_y+0.70,5.28)
            _add_textbox(slide,left,meta_y,10-left-right,0.28,meta.get("researcher",""),11,font,align=PP_ALIGN.CENTER)
            meta_y+=0.32
            for line in _supervisor_lines(meta):
                _add_textbox(slide,left,meta_y,10-left-right,0.27,line,10.5,font,align=PP_ALIGN.CENTER)
                meta_y+=0.29
            _add_textbox(slide,left,min(meta_y+0.08,6.58),10-left-right,0.28,meta.get("program",""),10.5,font,align=PP_ALIGN.CENTER)
        elif stype=="section":
            _add_textbox(slide,left,2.6,10-left-right,0.9,spec.get("title",""),title_pt,font,align=PP_ALIGN.CENTER)
            _add_textbox(slide,left,3.55,10-left-right,0.55,spec.get("subtitle",""),16,font,align=PP_ALIGN.CENTER)
        elif stype=="bullets":
            _add_textbox(slide,left,top,10-left-right,0.55,spec.get("title",""),title_pt,font)
            box=slide.shapes.add_textbox(Inches(left),Inches(1.25),Inches(10-left-right),Inches(5.4))
            tf=box.text_frame; tf.clear(); tf.word_wrap=True; tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
            for j,b in enumerate(spec.get("bullets",[])):
                p=tf.paragraphs[0] if j==0 else tf.add_paragraph()
                p.text=str(b); p.level=0; p.font.name=font; p.font.size=Pt(body_pt); p.font.color.rgb=RGBColor(0,0,0); p.space_after=Pt(9)
                # native bullet via XML
                p._p.get_or_add_pPr().insert(0, __import__("pptx").oxml.parse_xml('<a:buChar xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" char="•"/>'))
        elif stype in {"figure","two_figures"}:
            _add_textbox(slide,left,top,10-left-right,0.55,spec.get("title",""),title_pt,font)
            if stype=="figure":
                path=spec["figure"]["path"]; box_w=10-left-right; box_h=5.55
                with Image.open(path) as im: iw,ih=im.size
                scale=min(box_w/iw,box_h/ih); pw,pH=iw*scale,ih*scale
                slide.shapes.add_picture(path,Inches(left+(box_w-pw)/2),Inches(1.15+(box_h-pH)/2),width=Inches(pw),height=Inches(pH))
            else:
                gap=0.25; box_w=(10-left-right-gap)/2; box_h=5.45
                for j,obj in enumerate(spec["figures"]):
                    path=obj["path"]
                    with Image.open(path) as im: iw,ih=im.size
                    scale=min(box_w/iw,box_h/ih); pw,pH=iw*scale,ih*scale
                    bx=left+j*(box_w+gap)
                    slide.shapes.add_picture(path,Inches(bx+(box_w-pw)/2),Inches(1.15+(box_h-pH)/2),width=Inches(pw),height=Inches(pH))
            if spec.get("caption"):
                _add_textbox(slide,left,6.55,10-left-right,0.35,spec["caption"],caption_pt,font,align=PP_ALIGN.CENTER)
        elif stype=="literature_table":
            _pptx_literature_table(slide,spec,font,left,top,title_pt)
        elif stype=="methodology_flow":
            _pptx_methodology_flow(slide,spec,font,left,top,title_pt)
        elif stype=="closing":
            _add_textbox(slide,left,2.8,10-left-right,0.7,spec.get("title",""),title_pt,font,align=PP_ALIGN.CENTER)
            _add_textbox(slide,left,3.6,10-left-right,0.5,spec.get("subtitle",""),16,font,align=PP_ALIGN.CENTER)
        _add_textbox(slide,left,7.07,1.7,0.22,meta.get("date",""),footer_pt,font)
        _add_textbox(slide,3.0,7.07,4.0,0.22,meta.get("researcher",""),footer_pt,font,align=PP_ALIGN.CENTER)
        _add_textbox(slide,8.2,7.07,1.35,0.22,f"{idx}/{len(slides)}",footer_pt,font,align=PP_ALIGN.RIGHT)
    prs.save(out_path)
