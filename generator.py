import json
import random

random.seed(7)


def make_doc(prefix, vendor, amount, date):
    return {
        "id": f"{prefix}-{random.randint(1000, 9999)}",
        "vendor": vendor,
        "amount": amount,
        "date": date,
    }


vendors = ["Acme", "Globex", "Initech", "Umbrella"]
rows = []
for i in range(40):
    inv = make_doc(
        "INV", vendors[i % 4], round(random.uniform(100, 5000), 2), "2026-08-01"
    )
    po = make_doc("PO", vendors[i % 4], inv["amount"], "2026-07-20")
    rec = make_doc("REC", vendors[i % 4], inv["amount"], "2026-08-10")
    mismatch = i % 12 == 0  # ~8% seeded discrepancy
    if mismatch:
        rec["amount"] = round(rec["amount"] * 1.2, 2)
    rows.append(
        {"invoice": inv, "po": po, "receipt": rec, "expected_discrepancy": mismatch}
    )
with open("documents.json", "w") as f:
    json.dump(rows, f, indent=2)
print("generated 40 doc triples, ~8% mismatches")
