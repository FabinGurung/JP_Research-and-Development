from __future__ import annotations
import json, hashlib, math
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import fitz

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def render_pdf(pdf_path, out_dir, zoom=1.6):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    doc=fitz.open(pdf_path); pages=[]
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=fitz.Matrix(zoom,zoom),alpha=False)
        fn=out/f"page_{i+1:03d}.png"; pix.save(str(fn)); pages.append(fn)
    return pages

def make_montage(images, out_path, columns=3, thumb_w=480):
    ims=[]
    for p in images:
        im=Image.open(p).convert("RGB")
        ratio=thumb_w/im.width
        ims.append(im.resize((thumb_w,int(im.height*ratio))))
    if not ims: return None
    rows=math.ceil(len(ims)/columns); gap=20
    cell_h=max(im.height for im in ims)
    canvas=Image.new("RGB",(columns*thumb_w+(columns+1)*gap,rows*cell_h+(rows+1)*gap),"white")
    for i,im in enumerate(ims):
        r=i//columns;c=i%columns
        canvas.paste(im,(gap+c*(thumb_w+gap),gap+r*(cell_h+gap)))
    canvas.save(out_path,quality=92)
    return out_path

def qa_release(pdf_path,pptx_path,render_dir,montage_path,report_path):
    pages=render_pdf(pdf_path,render_dir)
    make_montage(pages,montage_path)
    report={
        "pdf":{"path":str(pdf_path),"sha256":sha256_file(pdf_path),"pages":len(pages)},
        "pptx":{"path":str(pptx_path),"sha256":sha256_file(pptx_path) if pptx_path and Path(pptx_path).exists() else None},
        "page_renders":[{"path":str(p),"sha256":sha256_file(p)} for p in pages],
        "montage":{"path":str(montage_path),"sha256":sha256_file(montage_path)},
        "structural_status":"PASS_IF_VALIDATOR_PASS",
        "visual_status":"REQUIRES_HUMAN_OR_MODEL_RENDER_REVIEW"
    }
    Path(report_path).write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
