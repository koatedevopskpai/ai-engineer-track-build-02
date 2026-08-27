CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  doc_id TEXT,
  vendor TEXT,
  amount NUMERIC,
  match3way BOOLEAN,
  status TEXT,
  decision TEXT,
  approver TEXT,
  decided_at TIMESTAMPTZ
);