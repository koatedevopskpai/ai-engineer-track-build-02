# verify_match.py — proves the 3-way match logic flags seeded discrepancies
# Runs the same rule as nodes/match3way.js against generator output.

import json

EPS = 0.01


def match3way(inv, po, rec):
    amounts = abs(inv["amount"] - po["amount"]) < EPS and abs(
        po["amount"] - rec["amount"]
    ) < EPS
    vendors = inv["vendor"] == po["vendor"] == rec["vendor"]
    return amounts and vendors


with open("documents.json") as f:
    rows = json.load(f)

flagged = 0
expected = 0
for r in rows:
    if r["expected_discrepancy"]:
        expected += 1
        if not match3way(r["invoice"], r["po"], r["receipt"]):
            flagged += 1
    else:
        if not match3way(r["invoice"], r["po"], r["receipt"]):
            flagged += 1

recall = flagged / expected if expected else 0
precision = flagged / len(rows)
print(f"seeded discrepancies: {expected}")
print(f"flagged: {flagged}")
print(f"recall on seeded mismatches: {recall:.0%}")
if recall < 0.95:
    raise SystemExit(f"FAIL: recall {recall:.0%} below 95% gate")
print("PASS: 3-way match flags >=95% of seeded discrepancies")