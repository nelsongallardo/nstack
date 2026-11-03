#!/usr/bin/env bash
# Small TypeScript + Supabase repo used by nstack eval cases.
set -euo pipefail
mkdir -p src test supabase/migrations
cat > package.json <<'EOF'
{ "name": "profiles-svc", "private": true, "type": "module", "scripts": { "test": "node --test test/*.test.ts" } }
EOF
cat > src/profile.ts <<'EOF'
export type Profile = { id: string; email: string; createdAt: string };

export function parseProfile(row: any): Profile {
  return { id: row.id, email: row.email, createdAt: row.created_at };
}
EOF
cat > test/profile.test.ts <<'EOF'
import { test } from "node:test";
import assert from "node:assert/strict";
import { parseProfile } from "../src/profile.ts";

test("parses a row", () => {
  const p = parseProfile({ id: "u1", email: "a@b.c", created_at: "2026-01-01T00:00:00Z" });
  assert.equal(p.id, "u1");
});
EOF
cat > supabase/migrations/20260101000000_profiles.sql <<'EOF'
create table public.profiles (
  id text primary key,
  email text not null,
  created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
EOF
cat > scripts.py <<'EOF'
import json, sys

def load(path):
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    print(load(sys.argv[1]))
EOF
git init -q -b main
git -c user.email=eval@example.com -c user.name=eval add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm "init"
