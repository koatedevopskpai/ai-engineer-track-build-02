# cost_report.py — assumptions-based ROI one-pager for Build 02

COST_PER_RUN = 0.04  # tokens for classify + extract + match (local Ollama ~ $0)
HOURS_SAVED_PER_DOC = 0.25  # 15 min manual matching
DOCS_PER_WEEK = 100
RATE_PER_HOUR = 50

weekly_cost = DOCS_PER_WEEK * COST_PER_RUN
weekly_hours = DOCS_PER_WEEK * HOURS_SAVED_PER_DOC
weekly_saving = weekly_hours * RATE_PER_HOUR

print(f"weekly cost: ${weekly_cost:.2f}")
print(f"hours saved: {weekly_hours}")
print(f"rate $50/hr -> weekly saving: ${weekly_saving:.2f}")
print(f"monthly saving: ${weekly_saving * 4:.2f} vs monthly cost: ${weekly_cost * 4:.2f}")
print(f"ROI (saving/cost): {weekly_saving / weekly_cost:.0f}x")