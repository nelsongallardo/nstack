---
name: python
description: Python rules for backend services, scripts, bots, and data jobs. Covers typing, pydantic at boundaries, uv and pyproject, pytest, async, and logging. Use when writing, editing, or reviewing any .py file or pyproject.toml.
---

# Python

Apply `types-and-boundaries` first. The repo's AGENTS.md / CLAUDE.md and its existing tooling win over this file.

## Tooling

- Use whatever the repo uses. For new projects: `uv` with `pyproject.toml` and a lockfile, `ruff` for lint and format, and `pyright` or `mypy --strict` for types.
- Run commands through the project env (`uv run pytest`, `uv run python -m …`). Never install into the system Python.
- Pin the Python version (`requires-python`, `.python-version`).

## Types

| Idea | Python |
|---|---|
| Parse at the boundary | Use `Model.model_validate(raw)` or `TypeAdapter(T).validate_python(raw)` for JSON, webhooks, and DB rows. Use `pydantic-settings` for env and config. `dict[str, Any]` stops at the parse. |
| Unknown fields | Inbound wire models: `ConfigDict(extra="ignore")`. Config: `extra="forbid"`. |
| Branded IDs | `UserId = NewType("UserId", str)`, created only inside a parse function. Or `Annotated[str, AfterValidator(check)]` in pydantic models. |
| Unions and variants | `Literal` tags plus pydantic discriminated unions (`Field(discriminator="kind")`). Use `match` with `case _: assert_never(x)` so the type checker catches a missing case. |
| State machines | An `Enum` state plus a transition dict `{(State, Event): State}`. Not a set of booleans. |
| Immutability | `@dataclass(frozen=True, slots=True)` or frozen pydantic models for domain values. |
| Derive from the source | Generate models from OpenAPI (`datamodel-code-generator`), or use ORM/SQLModel types. Don't keep hand-written parallel shapes. |
| Optional | Return `T | None` and handle it. Don't raise from a getter for a normal absence. |

No `# type: ignore` or `cast()` to silence a real error. Fix the type, or parse the value.

## Errors

- Raise specific exception classes. Callers catch the type, never match on message text.
- Catch only where you can handle or translate the error. Never write a bare `except:`. Never use `except Exception: pass`.
- At process boundaries (CLI `main`, worker loop, request handler), log with context and exit or respond with a stable code.

## Async and I/O

- Never call blocking I/O (`requests`, `time.sleep`, sync DB drivers) inside `async def`. Use `httpx.AsyncClient` and async drivers, or `asyncio.to_thread`.
- Every created task is awaited or tracked. Fire-and-forget tasks get garbage-collected and swallow errors.
- Set timeouts on every network call. Retry only idempotent operations, with backoff and a cap.
- A generator nobody iterates does no work. Watch for this in benchmarks and pipelines.

## Logging and config

- Use the `logging` module or `structlog` with structured fields (`log.info("sent", extra={"order_id": oid})`). No `print` in shipped code, except as a CLI's real output.
- Read env vars once, into a settings object, at startup.

## Scripts and jobs

- Make every job idempotent: upsert by natural key, write to a temp file then `os.replace`, and keep a checkpoint of processed IDs.
- Use `argparse` or `typer` for CLIs, with a `--dry-run` on anything destructive. Print machine-readable output (`--json`) when other tools consume it.
- Put the logic in importable pure functions, with a thin `if __name__ == "__main__":` shell.

## Tests (pytest)

- Test behavior through the public function or HTTP endpoint (FastAPI `TestClient`, a real DB via a fixture). See `tests`.
- Mock only third-party HTTP, at the transport layer (`respx`, `responses`), and assert the outbound payload.
- Use `pytest.mark.parametrize` for the failure-mode list. Use `tmp_path` for files. Never touch the real home directory or prod config.
