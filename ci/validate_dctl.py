#!/usr/bin/env python3
from pathlib import Path
import re,sys
p=next((Path(__file__).resolve().parents[1]/"dctl").glob("*.dctl"))
t=p.read_text()
checks=[
("__DEVICE__ float3 transform(" in t,"transform"),
("DEFINE_UI_PARAMS(" in t,"UI"),
(t.count("{")==t.count("}"),"braces"),
(t.count("(")==t.count(")"),"parentheses"),
(re.search(r"^(<<<<<<<|=======|>>>>>>>)",t,re.M) is None,"merge markers"),
]
for ok,n in checks: print(("[PASS] " if ok else "[FAIL] ")+n)
if not all(ok for ok,_ in checks): sys.exit(1)
