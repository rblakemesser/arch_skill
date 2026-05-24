# Session Reuse

Resume workers when continuity helps and the session is healthy.

## Resume By Default When

- The repair is directly related to the worker's previous slice.
- The worker understood the owning surface.
- The worker reported `SESSION HEALTH: healthy`.
- The session id was captured for the same runtime.

## Spawn Fresh When

- The worker is stuck, repeatedly wrong, or causing bugs.
- The repair crosses into a different owner boundary.
- The session id is missing, empty, or `UNRECOVERABLE`.
- The parent needs a cold implementation view.

## Hard Rules

- Never cross-resume between runtimes.
- Never use latest-session selection.
- Cursor Agent resumes only through `--resume <session_id>`.
- Codex resumes only through `codex exec resume <thread_id>`.
- Claude resumes only through `-r <session_id>`.
