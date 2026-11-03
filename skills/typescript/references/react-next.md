# React and Next.js (App Router)

These rules come from bugs seen in production apps, plus pstack. The repo's own conventions win. For example, a repo may use server actions for reads, or have no react-query. Follow it.

## Server/client boundary

- **Every export of a `'use server'` file is a public HTTP endpoint.** Inside each one, parse the input with the contract schema and check access. Put helpers in files without `'use server'`, or they become endpoints too.
- **Identity comes from the session on the server**, never from IDs, cookies, or form fields the browser sends. Derive the org and role from the session plus your API.
- **Filter private data on the server before it reaches the browser.** Hiding a chart element is not protection. Watch derived fields too: a "status" computed from a hidden value can reveal that value.
- Keep server-only modules server-only: `import 'server-only'`, no `NEXT_PUBLIC_` on secrets, and no DB or admin clients importable from client components. Enforce it with a lint rule or a boundary script, because conventions get copied wrong.
- Client components receive serializable props only. Pass IDs and plain data, not class instances or functions.

## Next 15+ APIs

- `await cookies()`, `await headers()`, `await params`, `await searchParams` on the server. In client pages, unwrap `params` with React `use()`.
- Middleware (`middleware.ts`, or `proxy.ts` in Next 16) refreshes the session and routes. It is not where authorization happens. Its matcher must exclude public routes and static assets, which have broken in practice.
- **Supabase SSR cookies:** in middleware, use the `getAll`/`setAll` pattern and write to both the request and the response. Dropping cookies there logs users out on refresh. On the server, call `getUser()` (which verifies the token) before trusting `getSession()`.

## Data and errors

- Keep the access check separate from the data fetch, so an outage isn't reported as "no permission". Map each failure to its own UI state: unauthorized, not found, failed, empty.
- Model loading state as a union (`{ kind: "loading" } | { kind: "ready", data } | { kind: "error", error }`), not `isLoading` + `data?` + `error?`.
- After a mutation, refresh exactly what changed (`revalidatePath`/`revalidateTag`, or `router.refresh()`). Don't refetch the world.
- Server actions return a result object for expected failures (`{ ok: false, code }`). Throw only for bugs.

## Client state

- **Reset client stores when the user changes.** A Zustand or global store survives sign-out and sign-in in the same tab, and leaked one user's answers to the next. Key stores by user ID, or clear them on auth change.
- Derive instead of syncing. Don't mirror props or server data into `useState` and keep them aligned with `useEffect`. Compute the value during render.
- `useEffect` is for synchronizing with external systems, not for data flow between components. Five `useState` booleans that move together belong in one `useReducer` with a union action.
- Never define components inside components, because each render gets a new identity and state resets.

## Forms

- Use one validation schema, shared by client hints and the server action. The server parse is the one that counts.
- Use `useActionState` / `useFormStatus` for pending and error state. Disable the submit button while pending, and make the action idempotent anyway, since double submits happen.

## UI quality (experience first)

- The user is whoever consumes the work. Choose user delight over implementation convenience. Ship fewer, polished features.
- Every async surface has designed loading, empty, error, and success states.
- Check with the real app, not with reasoning (`verify-ui`): the changed flow, keyboard focus, and a narrow viewport.
- Native browser behavior beats reimplementation. JS clones of sticky positioning, forwarded scroll or touch events, and mask hit-testing have produced bugs in every review pass. If you must reimplement, expect bugs and test with real input.
- Settle a novel interaction by prototyping 2 or 3 versions in throwaway HTML before building it (`design`).
