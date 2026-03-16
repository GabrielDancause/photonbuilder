import json

with open("real_data.json", "r") as f:
    data = json.load(f)

# Fix percentages (they were multiplied by 100 too many times)
for key, value in data.items():
    if "yield" in value and value["yield"] is not None:
        value["yield"] = value["yield"] / 100

with open("real_data.json", "w") as f:
    json.dump(data, f, indent=2)
