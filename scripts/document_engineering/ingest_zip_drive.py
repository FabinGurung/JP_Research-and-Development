#!/usr/bin/env python3
"""Private Google Drive ZIP ingestion. Default: read-only plan.

Run from an authenticated Colab/local session with authorized Drive access.
The source ZIP is immutable; no overwrite, delete, or public Git uploads.
"""
import argparse
import hashlib
import io
import json
import mimetypes
import pathlib
import zipfile

def escape_q(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")

def list_children(service, parent_id, name):
    q="'"+escape_q(parent_id)+"' in parents and name = '"+escape_q(name)+"' and trashed = false"
    items=[]
    token=None
    while True:
        p=service.files().list(q=q,spaces="drive",fields="nextPageToken,files(id,name,mimeType,size,md5Checksum,parents)",pageSize=100,pageToken=token).execute()
        items.extend(p.get("files",[]))
        token=p.get("nextPageToken")
        if not token:break
    return items

def folder(service, parent, name, execute):
    got=list_children(service,parent,name)
    if len(got)>1:
        raise RuntimeError("Ambiguous duplicate folder: "+name)
    if got:
        if got[0]["mimeType"]!="application/vnd.google-apps.folder":
            raise RuntimeError("Folder/file collision: "+name)
        return got[0]["id"]
    if not execute:
        return None
    return service.files().create(body={"name":name,"parents":[parent],"mimeType":"application/vnd.google-apps.folder"},fields="id").execute()["id"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="examples/document-engineering/private_ingest_routes.json")
    ap.add_argument("--execute",action="store_true",help="upload missing extracted files (otherwise dry run)")
    ap.add_argument("--report",default=None,help="PRIVATE local JSON report; do not commit it")
    a=ap.parse_args()
    cfg=json.loads(pathlib.Path(a.config).read_text(encoding="utf-8"))
    try:
        from google.colab import auth
        auth.authenticate_user()
    except ImportError:
        pass
    import google.auth
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
    creds,_=google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
    service=build("drive","v3",credentials=creds,cache_discovery=False)
    src=cfg["source_zip_file_id"]
    source_meta=service.files().get(fileId=src,fields="id,name,mimeType,size,parents").execute()
    if source_meta.get("mimeType")!="application/zip":
        raise RuntimeError("Source is not a ZIP archive")
    stream=io.BytesIO()
    download=MediaIoBaseDownload(stream,service.files().get_media(fileId=src),chunksize=8*1024*1024)
    done=False
    while not done:
        _,done=download.next_chunk()
    raw=stream.getvalue()
    if hashlib.sha256(raw).hexdigest()!=cfg["source_sha256"]:
        raise RuntimeError("Original ZIP SHA256 mismatch. STOP; no writes.")
    records=[]
    planned=0
    uploaded=0
    skipped=0
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries=[e for e in archive.infolist() if not e.is_dir()]
        if len(entries)!=102:
            raise RuntimeError("Unexpected entry count; no writes")
        for info in entries:
            logical=pathlib.PurePosixPath(info.filename)
            if logical.is_absolute() or ".." in logical.parts or len(logical.parts)<2 or "\\" in info.filename:
                raise RuntimeError("Unsafe source ZIP path")
            group=logical.parts[0]
            if group not in cfg["categories"]:
                raise RuntimeError("Unknown source category: "+group)
            parts=logical.parts[1:]
            # Two original source families share the exact filename Pradip adhikari.tex.
            # Keep both distinct, matching the existing completed A9 ingestion.
            if group in ("Experience letter", "Recommendation Letter"):
                parts=(group,)+parts
            data=archive.read(info)
            if len(data)>100_000_000:
                raise RuntimeError("Oversize entry")
            md5=hashlib.md5(data).hexdigest()
            sha=hashlib.sha256(data).hexdigest()
            parent=cfg["categories"][group]
            # Nested folders are created only on --execute; dry run cannot
            # pretend to resolve a not-yet-created nested path.
            for segment in parts[:-1]:
                resolved=folder(service,parent,segment,a.execute)
                if resolved is None:
                    parent=None
                    break
                parent=resolved
            name=parts[-1]
            if parent is None:
                exists=[]
            else:
                exists=list_children(service,parent,name)
            if len(exists)>1:
                raise RuntimeError("Duplicate collision: "+info.filename)
            record={"source_path":info.filename,"source_sha256":sha,"source_bytes":len(data),
                    "status":"PLAN","destination_id":None}
            if exists:
                obj=exists[0]
                if obj["mimeType"]=="application/vnd.google-apps.folder" or obj.get("md5Checksum")!=md5:
                    raise RuntimeError("Existing different file: "+info.filename)
                record["status"]="SKIP_IDENTICAL"
                record["destination_id"]=obj["id"]
                skipped+=1
            elif a.execute:
                mimetype=mimetypes.guess_type(name)[0] or "application/octet-stream"
                media=MediaIoBaseUpload(io.BytesIO(data),mimetype=mimetype,chunksize=8*1024*1024,resumable=True)
                metadata={"name":name,"parents":[parent],
                          "appProperties":{"a9_import_archive_sha":cfg["source_sha256"],
                                           "a9_zip_path_sha":hashlib.sha256(info.filename.encode()).hexdigest()}}
                created=service.files().create(body=metadata,media_body=media,fields="id").execute()
                check=service.files().get(fileId=created["id"],fields="id,name,parents,size,md5Checksum").execute()
                if check["name"]!=name or check.get("md5Checksum")!=md5 or parent not in check.get("parents",[]):
                    raise RuntimeError("Provider readback mismatch after upload")
                record.update(status="UPLOADED_VERIFIED",destination_id=created["id"])
                uploaded+=1
            else:
                planned+=1
            records.append(record)
    report={"source_zip_file_id":src,"source_sha256":cfg["source_sha256"],
            "file_count":len(records),"upload_count":uploaded,"identical_skip_count":skipped,
            "planned_count":planned,"mode":"EXECUTE" if a.execute else "DRY_RUN",
            "records":records}
    if a.report:
        pathlib.Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="records"},indent=2))
    if not a.execute:
        print("DRY RUN ONLY: use --execute after reviewing folder IDs and private access.")

if __name__=="__main__":
    main()
