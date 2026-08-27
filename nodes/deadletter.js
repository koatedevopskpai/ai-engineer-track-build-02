// nodes/deadletter.js — n8n Code node: error branch / dead-letter record
// Attach this node to the error output of the extract/match nodes.
return items.map((item) => {
  return {
    json: {
      ...item.json,
      deadletter: true,
      reason: item.json.reason || "extraction failed after retries",
      failed_at: new Date().toISOString(),
    },
  };
});