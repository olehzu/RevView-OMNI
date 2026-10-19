# RevView/OMNI charter

Read this at the start of every session. Each rule cites where it lives; follow the citation for the detail instead of guessing it.

## Where things are

- Requirements live in `docs/requirements/`: use cases (`use-cases.md`), business rules (`business-rules.md`), the specification (`software-requirements-specification.md`), the glossary (`project-glossary.md`), and open questions (`OPEN-ISSUES.md`).
- The architecture-of-record is `docs/design/architectural-design.md`.
- Work arrives as a build-context issue that cites a `UC-*`. Read that use case and everything it cites before planning.

## Stack

- Backend is a Python API, frontend is React with TypeScript, database is PostgreSQL (`CO-backend-language`, `CO-frontend-language`, `CO-database`, specification section 2.4).
- Add no other language, framework, or service without the team's agreement; the client must be able to run the system alone (`MNT-single-maintainer`, specification section 9.7).

## Hard constraints

- Use only the sandbox Jira, SVN, and Jenkins and synthetic data; never configure production instances (`CO-sandbox-development`, `BR-no-student-prod-access`).
- Never commit credentials, tokens, or connection strings; the repository may be public (`SEC-no-production-credentials-in-development`, `CO-public-repository`, architecture section 8.2.6).
- Reach Jira, SVN, and Jenkins only through the Integration Gateway's adapters (architecture sections 5.2 and 8.2.4).

## Conventions

- Error handling: translate every failure once at the trust boundary into a stable error code and a safe message; report unavailable Jira, SVN, or Jenkins evidence as unavailable, never as empty or passing (architecture section 8.2.1).
- Time: store timestamps in UTC, display them in the configured organization time zone, and get the current time from a replaceable clock so tests can set it (architecture section 8.2.2).
- API, code layout, validation, configuration, logging, persistence, auditing, and testing follow architecture sections 8.2.3 through 8.2.10.

## Working rules

- Use the glossary's terms in code, tests, and messages.
- Do not invent a rule, threshold, term, or permission. If the repository does not say it, list it as an assumption and ask; a question only the client can answer goes into `OPEN-ISSUES.md`.
