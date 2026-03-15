import json

with open("real_data.json", "r") as f:
    data = json.load(f)

# Fix percentages (they were multiplied by 100 too many times)
data["SCHD"]["yield"] = 3.3
data["MSTY"]["yield"] = 299.6
data["VYM"]["yield"] = 2.26
data["ULTY"]["yield"] = 131.53
data["JEPQ"]["yield"] = 10.58

with open("real_data.json", "w") as f:
    json.dump(data, f, indent=2)
