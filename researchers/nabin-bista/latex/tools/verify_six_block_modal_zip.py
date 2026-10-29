#!/usr/bin/env python3
"""Read-only Nabin six-block ZIP QA. Results are private evidence; do not publish output to Pages."""
import argparse, hashlib, io, json, re, zipfile, xml.etree.ElementTree as ET
N = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

def sha(blob):
    return hashlib.sha256(blob).hexdigest()

def workbook_info(blob):
    book = zipfile.ZipFile(io.BytesIO(blob))
    rel = {x.attrib["Id"]: x.attrib["Target"] for x in ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))}
    root = ET.fromstring(book.read("xl/workbook.xml"))
    sheets = []
    for item in root.findall(".//{%s}sheet" % N):
        path = rel[item.attrib[RID]].lstrip("/")
        if not path.startswith("xl/"):
            path = "xl/" + path
        sheets.append((item.attrib["name"], path))
    words = []
    if "xl/sharedStrings.xml" in book.namelist():
        for _, elem in ET.iterparse(book.open("xl/sharedStrings.xml"), events=["end"]):
            if elem.tag == "{%s}si" % N:
                words.append("".join(e.text or "" for e in elem.iter("{%s}t" % N)))
                elem.clear()
    return book, sheets, words

def cells(book, path, words, stop=100):
    rows = []
    for _, row in ET.iterparse(book.open(path), events=["end"]):
        if row.tag != "{%s}row" % N:
            continue
        number = int(row.attrib["r"])
        values = {}
        for c in row.findall("{%s}c" % N):
            v = c.find("{%s}v" % N)
            if v is None or v.text is None:
                continue
            val = v.text
            if c.get("t") == "s":
                val = words[int(val)]
            elif c.get("t") not in ("str", "inlineStr", "e"):
                try: val = float(val)
                except ValueError: pass
            values[c.attrib["r"]] = val
        rows.append((number, values))
        row.clear()
        if number >= stop:
            break
    return rows

def modal(book, path, words):
    rows = cells(book, path, words)
    head = next(((i, v) for i,v in rows if "SumUX" in v.values() and "SumUY" in v.values()), None)
    if head is None: return {"status":"NO_MODAL_HEADER"}
    headers = {str(value):re.match("[A-Z]+",key).group() for key,value in head[1].items()}
    result = {"status":"SOURCE_CELLS_ONLY","T1_seconds":None,"first_both_90_mode":None}
    for index,row in rows:
        if index < head[0]+2: continue
        mode = row.get(headers["Mode"]+str(index))
        if not str(mode).isdigit(): continue
        mode = int(mode)
        if mode == 1: result["T1_seconds"]=row.get(headers["Period"]+str(index)); result["T1_cell"]=headers["Period"]+str(index)
        x = row.get(headers["SumUX"]+str(index)); y = row.get(headers["SumUY"]+str(index))
        if result["first_both_90_mode"] is None and isinstance(x,float) and isinstance(y,float) and x>=.9 and y>=.9:
            result["first_both_90_mode"]=mode;result["dual_mass_cells"]=[headers["SumUX"]+str(index),headers["SumUY"]+str(index)]
    return result

def run(source):
    with open(source,"rb") as f: data=f.read()
    out={"archive_sha256":sha(data),"status":"SOURCE_ONLY_NOT_SCIENTIFIC_APPROVAL","files":[],"modal_cases":[]}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if archive.testzip() is not None: raise ValueError("ZIP CRC failure")
        for item in archive.infolist():
            if item.is_dir(): continue
            raw = archive.read(item)
            out["files"].append({"path":item.filename,"sha256":sha(raw),"bytes":len(raw)})
            if "Modal Participating" not in item.filename or not item.filename.endswith(".xlsx"):continue
            book,sheets,words=workbook_info(raw)
            for name,path in sheets:
                record=modal(book,path,words);record.update({"workbook":item.filename,"sheet":name})
                out["modal_cases"].append(record)
            book.close()
    out["modal_complete"]=len(out["modal_cases"])==24 and all(x.get("T1_seconds") is not None for x in out["modal_cases"])
    return out

if __name__ == "__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--zip",required=True);ap.add_argument("--out",required=True)
    args=ap.parse_args();result=run(args.zip)
    with open(args.out,"w") as f:json.dump(result,f,indent=2)
    print("ZIP_QA_PASS MODAL=%d COMPLETE=%s" % (len(result["modal_cases"]),result["modal_complete"]))
