# Phase 0 Audit — Baseline

Repository: nan-avan-alla/CeWiL, branch main.
Product: India-first, global-ready civil engineering operations platform. Full Engineering Operations MVP. Microservices target with monorepo implementation initially.

## Recovered baseline capabilities
FastAPI, ten-domain specialist registry, advisory keyword risk triage, SQLite evidence/workflow records, standards source metadata and knowledge entries, document upload/extraction, filename version chain, text diff and SQLite FTS5 search.

## Verified CI
Initial audit run 4 exposed two defects: document search route shadowing and standards-source column ordering. Both were fixed in commits 3f409d9 and c64b7ec. Latest verified CI run 7 passed: https://github.com/nan-avan-alla/CeWiL/actions/runs/45431273237.

## Material gaps
No authentication/RBAC, project-level access enforcement, production database/migrations, verified backup/restore, upload malware scanning/quarantine, semantic/vector RAG, CAD geometry or visual revision comparison, production observability, infrastructure or disaster recovery.

## Exit criteria
- [x] Product decisions captured.
- [x] Service boundaries documented.
- [x] Current capabilities and gaps inventoried.
- [x] CI failure causes identified.
- [x] CI defects fixed and latest run green (run 7).
- [x] Existing document-search and standards-source regression tests pass in the green CI run.
- [x] MVP acceptance gates and threat-model requirements documented.
- [ ] Identity, authorisation and project isolation implemented and independently tested (Phase 1 remains).
