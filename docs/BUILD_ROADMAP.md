# CeWiL Engineering Operating System — Build Roadmap

## Product decisions
- India first, global-ready architecture.
- Full Engineering Operations MVP.
- Microservices target architecture; monorepo initially, independently buildable/deployable service boundaries.

## Phases
0. Audit baseline, scope, threat model, acceptance criteria.
1. Foundation: configuration, migrations, typed contracts, authentication/RBAC, project isolation, audit trail, observability and tests.
2. Project/document control: projects, members, files, revisions, provenance.
3. India-first standards and governed knowledge: jurisdiction, editions, amendments, review states, hybrid retrieval and citations.
4. Deterministic engineering services: units, quantities, BOQ, rate analysis and reproducible calculation evidence.
5. Construction operations: RFI, ITP, NCR, inspections, submittals, change and action workflows.
6. Specialist agents: bounded tools, orchestrator, evidence and approval gates.
7. Production platform: IaC, CI/CD, secrets, monitoring, backup/restore, security review and rollback.
8. Pilot and scale with parallel professional review.

## Baseline audit
- A previous roadmap commit was created without the existing base tree; the recovery commit restores the prior application tree and retains roadmap documentation.
- CI run 4 failed: 10 passed, 2 failed. Document search endpoint shadowed by dynamic document-id route (404); standards-source insert column order mismatched SQLite schema (NOT NULL url).
- Run: https://github.com/nan-avan-alla/CeWiL/actions/runs/45424987788
- Fix both defects and verify green CI before Phase 0 completion.

## Launch constraints
No public production deployment until authentication, authorisation, project isolation, upload scanning, secrets management, durable storage, backups, monitoring, security review and rollback are implemented and tested. Engineering outputs remain drafts requiring qualified review.
