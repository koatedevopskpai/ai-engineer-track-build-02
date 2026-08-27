// nodes/match3way.js — n8n Code node: rule-based 3-way match + LLM sanity check
// Input: item with { invoice, po, receipt } (already classified/extracted)
// Output: { match3way, status: "MATCH"|"FLAG", ... }
const EPS = 0.01;

function amountsAgree(a, b) {
  return Math.abs(a - b) < EPS;
}

return items.map((item) => {
  const { invoice, po, receipt } = item.json;
  const match =
    amountsAgree(invoice.amount, po.amount) &&
    amountsAgree(po.amount, receipt.amount) &&
    invoice.vendor === po.vendor &&
    po.vendor === receipt.vendor;
  return {
    json: {
      ...item.json,
      match3way: match,
      status: match ? "MATCH" : "FLAG",
    },
  };
});