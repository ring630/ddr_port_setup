import numpy as np
import json

data = {}

data["ldq"] = {}
ldq_mapping = ["G9", "G3", "F8", "F4", "J9", "J3", "J8", "J4"]
for i in np.arange(8):
    data["ldq"]["dq" + str(i)] = ldq_mapping[i]

data["udq"] = {}
udq_mapping = ["C9", "C3", "B8", "B4", "E9", "E3", "E8", "E4"]
for i in np.arange(8, 16):
    data["udq"]["dq" + str(i)] = udq_mapping[i-8]

data["ca"] = {}
ca_mapping = ["N4", "N8", "P4", "P8", "N3", "N9", "P3", "P9", "R4", "R8", "T3", "T9", "T4", "T8"]
for i in np.arange(14):
    data["ca"]["ca" + str(i)] = ca_mapping[i]

data["dqs"] = {}
data["dqs"]["ldqs_p"] = "G4"
data["dqs"]["ldqs_n"] = "H4"
data["dqs"]["udqs_p"] = "C4"
data["dqs"]["udqs_n"] = "D4"

data["ck"] = {}
data["ck"]["ck_p"] = "L8"
data["ck"]["ck_n"] = "M8"

data = json.dumps(data, indent=4)
with open("template_ddr5_x16.json", "w", encoding="utf-8") as f:
    f.write(data)

print(data)
