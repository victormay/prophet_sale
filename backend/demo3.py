import json
import pandas as pd
from pathlib import Path
from datetime import datetime


data = pd.read_excel("./demo.xlsx")

# print(data.head())
print(data.info())
print(data.describe())

bianmas = data.value_counts(["wupinbianma", "wupinmingcheng"]).head(20).reset_index()["wupinbianma"]

data = data[data["wupinbianma"].isin(bianmas)].reset_index(drop=True)

print(data.head(50))