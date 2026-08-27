// nodes/classify.js — n8n Code node: classify document type + vendor
// Input: item with { id, vendor, amount, date }
// Output: { category, vendor, ...original }
return items.map((item) => {
  const id = item.json.id || "";
  const category = id.startsWith("INV")
    ? "invoice"
    : id.startsWith("PO")
      ? "po"
      : "receipt";
  return {
    json: {
      ...item.json,
      category,
      vendor: item.json.vendor || "unknown",
    },
  };
});