# The agentic invariant method, applied to TagStream

This repo adopts a small, durable "operating method" for any agent (or human)
working on it. It is the same method used on the maintainers' other projects,
adapted here for a **command-line, local-ML tool** rather than a web app.

## What the method is

- **Context lives in the repo.** Project memory is `CLAUDE.md` + `AGENT_RULES.md` +
  `docs/context/*` — committed, so it survives a fresh clone and is not lost between
  sessions. Read the full files, not just the index summaries.
- **Rules have triggers.** A rule earns its place only if a future agent can tell
  *when* it fires and *what to do*. No "always be careful."
- **Verify before commit.** Run the tests; for pipeline changes, actually run the CLI
  on a sample clip. Typecheck/lint/"it imports" is not proof it works.
- **Don't claim what isn't shipped.** Capability claims in the README/description
  must be backed by code + a run. (This is why "visual verification" is flagged as
  not-yet-implemented.)
- **Leave a handoff** when stopping mid-task, and **kill recurring bug classes** with
  a guard/test in the same change as the fix.

## How it is adapted (this project vs the web apps it came from)

The transferable parts are the same; the **risk surfaces are different**:

- Web-app *data confidentiality / RLS* → here, **honest, correct tag output** and not
  over-claiming capabilities.
- Web-app *schema / migrations* → here, the **tag output contract** (count, dedup,
  normalization) and **dependency/setup reproducibility**.
- Web-app *auth / secrets at the boundary* → here, **external-binary (ffmpeg) and
  local-model assumptions**, plus `.env` discipline if a cloud API is ever added.
- Web-app *deploy safety* → here, **resource safety on large videos** (temp cleanup,
  no whole-file-in-memory) and a **reproducible Mac/venv run**.
- Web-app *"render the page to verify"* → here, **run the CLI on a real clip** and
  eyeball the tags; and **test the deterministic glue, not the model outputs**.

## Practical next use

When a task starts, don't ask "what did we discuss in chat?" Ask:

1. Which surface does this touch — sampling/ffmpeg, models, the tag output, or a
   capability claim?
2. Which context file owns it (`CLAUDE.md` / `PROJECT_INVARIANTS.md`)?
3. What run or test proves the change (CLI on a clip? a glue unit test)?
4. Is any claim still aspirational (e.g. visual verification) or any path still
   unverified (large-file temp cleanup)?
