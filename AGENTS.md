# RevView/OMNI charter

Read this at the start of every session. Each rule cites where it lives; follow the citation for the detail instead of guessing it.

## Where things are

- Requirements live in `docs/requirements/`: use cases (`use-cases.md`), business rules (`business-rules.md`), the specification (`software-requirements-specification.md`), the glossary (`project-glossary.md`), and open questions (`OPEN-ISSUES.md`).
- The architecture-of-record is `docs/design/architectural-design.md`.
- Work arrives as a build-context issue that cites a `UC-*`. Read that use case and everything it cites before planning.

## Stack

- Backend is a Python API, frontend is React with TypeScript, database is PostgreSQL (`CO-backend-language`, `CO-frontend-language`, `CO-database`, specification section 2.4).
- Add no other language, framework, or service without the team's agreement; the client must be able to run the system alone (`MNT-single-maintainer`, specification section 9.7).

## Things the agent must not do

- Never add a dependency (a package, library, tool, or service) until a person has confirmed it exists and is the one we meant; name it and ask instead of installing it (`.claude/commands/implement.md`, Phase 1 step 6).
- Never remove the `Co-Authored-By` trailer from a commit (`.claude/commands/implement.md`, Phase 1 step 6).
- Use only the sandbox Jira, SVN, and Jenkins and synthetic data; never configure production instances (`CO-sandbox-development`, `BR-no-student-prod-access`).
- Never commit credentials, tokens, or connection strings; the repository may be public (`SEC-no-production-credentials-in-development`, `CO-public-repository`, architecture section 8.2.6).
- Reach Jira, SVN, and Jenkins only through the Integration Gateway's adapters (architecture sections 5.2 and 8.2.4).

## Conventions

- Error handling: translate every failure once at the trust boundary into a stable error code and a safe message; report unavailable Jira, SVN, or Jenkins evidence as unavailable, never as empty or passing (architecture section 8.2.1).
- Time: store timestamps in UTC, display them in the configured organization time zone, and get the current time from a replaceable clock so tests can set it (architecture section 8.2.2).
- API, code layout, validation, configuration, logging, persistence, auditing, and testing follow architecture sections 8.2.3 through 8.2.10.
- Static analysis: from the repository root, run both gate chains: `(cd backend && ruff format --check . && ruff check . && mypy app tests && pytest)` and `(cd frontend && npm run format:check && npm run lint && npm run typecheck && npm test && npm run build)`; a baseline only shrinks; never weaken a check to make it pass without saying so in the pull request. See [architecture section 8.2.11](docs/design/architectural-design.md#8211-static-analysis) for setup, tool choices, and finding resolution.

## Workflow

- One agent per sub-issue, each in its own worktree and branch (`claude --worktree <name>`) and ending in its own pull request.
- Fan out only after the shared code the leaves depend on is merged.
- Never split one use case's layers across agents.
- No more agents running than pull requests you will review that day.

## Working rules

- Use the glossary's terms in code, tests, and messages.
- Do not invent a rule, threshold, term, or permission. If the repository does not say it, list it as an assumption and ask; a question only the client can answer goes into `OPEN-ISSUES.md`.
