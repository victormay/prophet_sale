import json
import pandas as pd
from pathlib import Path
from datetime import datetime


root = Path("./data/rawdata")

files= list(root.glob("*.json"))
sorted_files = sorted(files, key=lambda x: datetime.strptime(x.stem.split("_")[-1], "%Y-%m-%d"))

total = None

for i in sorted_files:
    with open(i, "r", encoding="utf8")as f:
        js_data = json.load(f)
    pd_data = pd.DataFrame(js_data["items"], columns=["yewuriqi", "wupinbianma", "wupinmingcheng", "caigoushuliang", "kucundanwei"])
    a = pd_data.groupby(["wupinbianma", "wupinmingcheng", "kucundanwei", "yewuriqi"]).sum().reset_index()
    a = a[["yewuriqi", "wupinbianma", "wupinmingcheng", "kucundanwei", "caigoushuliang"]]
    
    if total is None:
        total = a
    else:
        total = pd.concat([total, a], ignore_index=True)

total.to_excel("demo.xlsx", index=False)