---
name: typescript
description: TypeScript rules for backend and frontend code (Node, NestJS, Next.js, React). Covers types, narrowing, schemas, and React/Next server-client boundaries. Use when writing, editing, or reviewing any .ts or .tsx file.
---

# TypeScript

Apply `types-and-boundaries` first. The repo's AGENTS.md / CLAUDE.md and its existing conventions win over this file.

Examples for every rule: `references/patterns.md`. React and Next.js: `references/react-next.md`.

## Types

| Rule | Summary |
|---|---|
| Discriminated unions | Model variants with a `kind` literal so impossible states can't be represented. No optional-field bags. Pick one discriminant name per repo and stick to it. |
| Branded types | `string & { readonly __brand: "OrgId" }` for IDs that get mixed up. A brand comes from a verifying type guard (`input is OrgId`), never from `as`. |
| Constructive modeling | `[T, ...T[]]` for non-empty, `[T, T][]` for pairs, start plus duration for a range. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown` until parsed. |
| Schemas before guards | Use the repo's schema library (zod) and infer types from it (`z.infer`). Use `safeParse` when failure is an expected branch. Don't add a new schema dependency for one guard. |
| No `as` | Every `as` is a runtime crash waiting. Cast only after validation. |
| Narrowing order | Discriminant switch > `in` > `typeof`/`instanceof` > user-defined guard > `as`. |
| Type guards | They must verify the claim. A lying guard is worse than `as`, because the bug hides behind a name that says it's safe. Name them `isX` / `hasX`. |
| Exhaustiveness | `default: { const _exhaustive: never = x; return _exhaustive; }` so the compiler errors when a variant is added. |
| `satisfies` over `as` | Checks the value without widening its literal types. |
| Derive, don't redeclare | Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof`, and generated types before declaring a new interface. |
| Object args | Pass an object when two arguments share a type or there are more than two. Positional is fine for one or two distinct types and on hot paths. |
| Strict | `strict: true` in each project's tsconfig. Don't loosen it to make an error go away. |

**Removing an `as`:**

- Missing discriminant → add one and switch to a union.
- Source type too wide (`Record<string, unknown>`) → narrow it.
- Untyped boundary → parse with the schema that owns the shape.
- Genuinely inexpressible → a branded type or `satisfies`.

## Errors and async

- Every promise is awaited, returned, or explicitly handed off with an error handler. A floating promise is work that may never happen, and a benchmark can time it as zero.
- Throw `Error` subclasses or return a result union. Callers branch on the error type or code, never on message text.
- Catch only where you can handle the error or translate it at a boundary. Never `catch {}`.
- Keep error bodies at the API boundary to a stable code. Map them to UI messages on the client side.

## Runtime and logging

- Structured logger with enough context to debug from an ID. No `console.log` in shipped code.
- Read env vars once, at startup, through a parsed config object. Never `process.env.X` deep in the code.
- Secrets never cross into client bundles. In Next.js, only `NEXT_PUBLIC_*` reaches the browser, and nothing secret is ever `NEXT_PUBLIC_*`.

## Tests

Don't mock what you can run. Use the framework's real test primitives (supertest against the Nest app, a real DB) and check UI in a running build (`verify-ui`). See `tests`.

## Backend (NestJS / Node)

- Validate at the edge with the contract schema (zod) via a pipe, interceptor, or decorator. Handlers receive typed input and return plain values.
- Authorization is declared per route and enforced by a guard that fails closed: an unannotated route is denied.
- Services hold the business logic as plain functions or classes with no framework imports. Keep framework types (`Request`, `Response`) out of them.
- One transaction per request where needed, with statement and idle timeouts. Never hold a transaction open across an external call.
- Generate the API client from the contract (OpenAPI, then a typed fetch client), and gate drift in CI.
