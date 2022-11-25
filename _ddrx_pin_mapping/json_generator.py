import pandas as pd
import json


ex = pd.ExcelFile("JEDEC_DDR_INFO.xlsx")
ddr4_x16 = ex.parse("DDR4_X16")

data = {}

for _, i in ddr4_x16.iterrows():
    if i.group not in data:
        data[i.group] = {i.pin_name: i.pin_number}
    else:
        data[i.group][i.pin_name] = i.pin_number

json_object = json.dumps(data, indent=4)

with open("ddr4_x16.json", "w") as f:
    f.write(json_object)