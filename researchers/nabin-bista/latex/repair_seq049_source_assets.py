#!/usr/bin/env python3
"""Non-destructive recovery of two historical Nabin SEQ049 figure PDFs."""
from pathlib import Path
import zipfile, hashlib, argparse

ORIGINAL_SHA = "99bed6893ddf0115cfc738ce7b5213794ba3f032b86750e0ca3537f36363e725"
FILES = {
 "figures/ch3/hospital_2d_plan.pdf": "a4ec6bd8aa016418c8b07b4a509624081f12f36c6baccb26486b17f40d6b0fa1",
 "figures/ch3/research_workflow_seq44.pdf": "8f76e8736e9ac08cd7ddfe16c0d4dc0011cf0ee0cc651cf98973e0d786c93403",
}
def sha(b): return hashlib.sha256(b).hexdigest()
def repair(p049,p046,out):
 p049,p046,out=map(Path,(p049,p046,out))
 if out.exists() or out.resolve() in (p049.resolve(),p046.resolve()): raise ValueError("Refusing overwrite")
 if sha(p049.read_bytes())!=ORIGINAL_SHA: raise ValueError("Incorrect SEQ049 ZIP SHA")
 with zipfile.ZipFile(p049) as src,zipfile.ZipFile(p046) as older:
  if set(FILES).intersection(src.namelist()): raise ValueError("Figures already present")
  assets={}
  for name,expected in FILES.items():
   assets[name]=older.read(name)
   if sha(assets[name])!=expected: raise ValueError("Historical asset mismatch "+name)
  with zipfile.ZipFile(out,"w") as target:
   for entry in src.infolist(): target.writestr(entry,src.read(entry))
   for name,b in assets.items(): target.writestr(older.getinfo(name),b)
 with zipfile.ZipFile(p049) as src, zipfile.ZipFile(out) as dst:
  assert len(dst.namelist())==len(src.namelist())+2
  assert all(dst.read(name)==src.read(name) for name in src.namelist())
 return sha(out.read_bytes())
if __name__=="__main__":
 a=argparse.ArgumentParser()
 a.add_argument("--seq049",required=True);a.add_argument("--seq046",required=True);a.add_argument("--out",required=True)
 n=a.parse_args()
 print("SEQ049_SOURCE_REPAIR_PASS sha256="+repair(n.seq049,n.seq046,n.out))
