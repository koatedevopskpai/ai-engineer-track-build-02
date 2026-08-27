// nodes/approval.js — n8n Code node: record the human decision after the Wait node
// The Wait node pauses the workflow; this node runs after a human approves/rejects.
// In n8n, bind the decision via the Wait resume payload: $json.approved, $json.approver
return items.map((item) => {
  const j = item.json;
  const approved = j.approved === true || j.approved === "true";
  return {
    json: {
      ...j,
      decision: approved ? "APPROVED" : "REJECTED",
      approver: j.approver || "admin",
      decided_at: new Date().toISOString(),
    },
  };
});