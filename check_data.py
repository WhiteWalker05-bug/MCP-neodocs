import json

with open("scans.json") as f:
    scans = json.load(f)

print("Number of scans:", len(scans))
print("First scan:", scans[0])

for scan in scans:
    print(scan["scan_id"], scan["scan_date"])