---
name: supabase
description: Work safely with Supabase and Postgres, including migrations (ordering, naming, applied state per environment), RLS policies and grants, auth on the server, local vs preview vs production, and SQL functions. Use when writing or reviewing a migration, a policy, a grant, a SQL function, Supabase auth code, or seed data, or when deploying DB changes.
---

# Supabase / Postgres

The repo's AGENTS.md and its migration docs win over this file. Read them first. Many repos lock down roles and access paths in ways that differ from Supabase defaults.

## Environments

- Know which database each command hits before running it: local, preview/branch, or production. Print the target first (`supabase status`, the host from the connection string). Never point a local script at production.
- Use the repo's documented local setup (`supabase start`, a disposable Postgres from a script, or PGlite in tests). Never install a database server or other system-level dependency without first checking the documented setup and saying why it's needed.
- Production migrations, grants, and data changes are pause-first actions unless the user granted them for this run.

## Migrations

- **Never edit a migration that has been applied anywhere** (local teammates, preview, prod). Write a new one.
- **Ordering:** a new migration's timestamp must sort after everything already applied in every environment it will reach. Before merging, check the applied list (`supabase migration list`, or the migration table on preview and prod). When parallel branches add migrations, rename unapplied ones so they sort after the latest applied. Out-of-order files get skipped or fail.
- **Idempotent and re-runnable where possible:** `create … if not exists`, `drop … if exists`, `create or replace function`. Data backfills upsert by natural key.
- **Data changes are separate from schema changes**, and destructive steps happen in a later migration than the code that stops using them (expand → migrate → contract).
- Release order: migrations → API → web. Code that needs a new column ships after the column exists.
- Big tables: avoid long locks. Add a column nullable first, backfill in batches, then add the constraint. Create indexes `concurrently` (outside a transaction).
- **Test it:** apply it to a fresh local DB, then read the affected rows or objects back. Run the repo's DB integration tests. A migration that passes on an empty DB can still fail on real data, so check it against a realistic seed.

## Access control

- **RLS on every table that holds user data**, with a policy per operation (`select`, `insert`, `update`, `delete`). An `update` policy needs both `using` and `with check`.
- Policies derive the caller from the session (`auth.uid()`, or a context function the app sets), never from a column the client controls.
- **Grants are part of the security model.** New tables need explicit grants for the roles the app uses. Grant the minimum. Don't hand broad rights to `anon`, `authenticated`, `service_role`, or `PUBLIC` unless the repo's design calls for it. A table with RLS but no grant fails closed, and a broad grant with a weak policy fails open.
- `security definer` functions: set `search_path` explicitly, check the caller inside, and grant `execute` narrowly.
- The service role key never reaches a browser, a client bundle, or logs.
- **Test policies as the role:** `set local role <role>; set local request.jwt.claims = '…';` then try both the allowed and the forbidden read or write. A policy you never saw deny proves nothing.

## Types and SQL

- Match the ID column type exactly (`text` vs `uuid`). Cast parameters explicitly in raw SQL.
- Compare emails with `lower(btrim(email))`, and store them normalized.
- Use `timestamptz`, never `timestamp`.
- Give each transaction a `statement_timeout` and `idle_in_transaction_session_timeout`, so a dropped request can't hold locks.
- Never hold a transaction open across an HTTP call or other external I/O.

## Auth (SSR)

- Server code verifies the user with `auth.getUser()` before trusting a session. `getSession()` alone reads an unverified cookie.
- In Next.js middleware/proxy, use the `getAll`/`setAll` cookie pattern on both the request and the response. Dropped cookies log users out on refresh.
- Sign-out runs on the server (a route or action), and clears client stores (see `typescript` → `react-next.md`).

## Reviewing a DB change

Check, in order:

1. Ordering against applied migrations.
2. Grants and policies for every new table or function, tested as the role.
3. Lock and backfill behavior on real table sizes.
4. Whether old code still running during the deploy works against the new schema.
