# Phase 0 Audit — Baseline

Repository: nan-avan-alla/CeWiL, branch main.
Product: India-first, global-ready civil engineering operations platform. Full Engineering Operations MVP. Microservices target with monorepo implementation initially.

## Recovered baseline capabilities
FastAPI, ten-domain specialist registry, advisory keyword risk triage, SQLite evidence/workflow records, standards source metadata and knowledge entries, document upload/extraction, filename version chain, text diff and SQLite FTS5 search.

## Verified CI
Run 4 failed with 10 passed and 2 failed. Known defects: document search route is shadowed by dynamic document-id route; standards source insertion order does not match SQLite schema. See https://github.com/nan-avan-alla/CeWiL/actions/runs/45424987788.

## Material gaps
No authentication/RBAC, project-level access enforcement, production database/migrations, verified backup/restore, upload malware scanning/quarantine, semantic/vector RAG, CAD geometry or visual revision comparison, production observability, infrastructure or disaster recovery.

## Exit criteria
- [x] Product decisions captured.
- [x] Service boundaries documented.
- [x] Current capabilities and gaps inventoried.
- [x] CI failure causes identified.
- [ ] CI defects fixed and latest run green.
- [ ] MVP acceptance tests and threat model reviewed.
