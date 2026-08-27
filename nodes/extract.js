// nodes/extract.js — n8n Code node: extract structured fields (JSON schema)
// In production, POST the raw text to Ollama /api/chat or OpenRouter with
// response_format=json_schema. This node returns the schema shape for the
// structured-output contract so the 3-way match is deterministic in the demo.
const schema = {
  type: "object",
  properties: {
    invoice_no: { type: "string" },
    total: { type: "number" },
    vendor: { type: "string" },
    date: { type: "string" },
  },
  required: ["invoice_no", "total", "vendor"],
};

// Demo passthrough mapping from the classified item.
return items.map((item) => {
  const j = item.json;
  return {
    json: {
      ...j,
      extracted: {
        invoice_no: j.id,
        total: j.amount,
        vendor: j.vendor,
        date: j.date,
      },
      _schema: schema,
    },
  };
});