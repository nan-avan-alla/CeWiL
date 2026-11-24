# CeWiL Engineering Operating System — Build Roadmap

## Product objective
Build a governed engineering operations platform that organises project information, evidence, workflows, calculations, and specialist assistance. It is not an autonomous engineer, statutory authority, or substitute for qualified professional judgement.

## Delivery principles
1. Correctness and traceability before feature breadth.
2. Every engineering output carries inputs, units, assumptions, method/version, source references, and review state.
3. Jurisdiction and source edition are explicit; never silently infer code applicability.
4. Deterministic calculation services are separated from language-model interpretation.
5. Human approval is required for safety-critical and regulated decisions.
6. Tenant isolation, security, backups, and auditability are designed before production data is accepted.
7. Every release is tested, reproducible, observable, and reversible.

## Workstreams and gates

### Phase 0 — Baseline audit and product definition
- Inventory every endpoint, module, dependency, schema, and existing test.
- Run the current CI suite and capture failures; do not treat a commit as tested until CI is green.
- Define MVP user roles, project lifecycle, first target customer workflow, and supported jurisdiction.
- Establish architecture decisions, threat model, data classification, and acceptance criteria.
**Exit gate:** reproducible local setup, green baseline tests, agreed MVP scope, architecture decision records.

### Phase 1 — Engineering-grade foundation
- Consolidate database configuration and implement migrations rather than import-time schema mutation.
- Introduce typed API contracts, consistent error handling, pagination, idempotency where needed, and structured logs.
- Add database constraints, indexes, transaction boundaries, and concurrency tests.
- Add authentication, role-based permissions, project-level authorisation, audit events, and secure upload handling before handling real client data.
- Add unit, integration, API, migration, and security tests.
**Exit gate:** access-control tests pass; no cross-project data leakage; clean migration and backup/restore tests.

### Phase 2 — Project and document control
- Project, organisation, member, role, location, discipline, and revision entities.
- Document register, metadata, checksum, revision relationships, retention, and immutable source originals.
- PDF/DOCX/XLSX/image ingestion with extraction status, page/sheet provenance, and OCR quality signals.
- Drawing register and manual drawing metadata first; CAD/DWG/DXF parsing only after a supported toolchain is selected.
- Visual and text revision comparison with explicit limitations and reviewer confirmation.
**Exit gate:** source-to-extract traceability and tested revision workflow.

### Phase 3 — Standards and governed knowledge
- Source catalogue with jurisdiction, publisher, edition, amendments, effective dates, and official-source status.
- Ingestion pipeline that records exact source document, page, clause, extraction version, and content hash.
- Review and approval workflow for knowledge entries; separate unverified, reviewed, superseded, and withdrawn states.
- Hybrid retrieval: keyword plus vector search, jurisdiction filters, reranking, and citations.
- Evaluation set for retrieval accuracy, citation correctness, stale-source handling, and refusal when evidence is insufficient.
**Exit gate:** every answer is traceable to reviewed source passages; unsupported claims are surfaced.

### Phase 4 — Deterministic engineering services
- Unit system and dimensional validation.
- Independently verified quantity calculations and rate-analysis engine.
- Versioned calculation templates, assumptions, formulas, input/output records, and test vectors.
- BOQ generation with source rates, location, date, wastage, exclusions, and reviewer sign-off.
- Structural and life-safety calculations only after domain-specific validation plans and qualified engineering governance exist.
**Exit gate:** independent benchmark cases pass; calculations are reproducible and reviewable.

### Phase 5 — Workflows and collaboration
- RFI, submittal, ITP, inspection, NCR, site instruction, change, and action workflows.
- Configurable status transitions, assignment, due dates, comments, attachments, notifications, and complete event history.
- Approval matrix and electronic acknowledgement with attributable identity.
- Project dashboards, overdue items, evidence completeness, and exportable reports.
**Exit gate:** a real pilot workflow can be completed end-to-end with audit history.

### Phase 6 — Specialist agents and orchestration
- Define bounded responsibilities, input contracts, allowed tools, and prohibited decisions for each specialist.
- Orchestrator plans tasks, gathers evidence, calls deterministic tools, and returns structured drafts.
- Require citations, uncertainty statements, risk flags, and human approval for controlled actions.
- Add adversarial tests for prompt injection in uploaded documents, fabricated citations, unsafe recommendations, and cross-project access.
**Exit gate:** agents cannot bypass permissions, evidence requirements, or approval gates.

### Phase 7 — Production platform and operations
- Select hosting, managed relational database, object storage, vector service, secrets manager, and network boundaries.
- Infrastructure as code, separate dev/test/production environments, CI/CD approvals, rollback, and disaster recovery.
- Monitoring, traces, metrics, cost budgets, alerting, backups, restore drills, retention, and incident response.
- Security review, dependency scanning, container scanning, penetration testing, privacy and legal review.
**Exit gate:** operational readiness review and explicit production go/no-go approval.

### Phase 8 — Pilot, validation, and scale
- Pilot with one carefully selected project and consenting users.
- Run outputs in parallel with existing professional processes; compare quality and time saved.
- Collect defects, retrieval misses, calculation discrepancies, user feedback, and safety incidents.
- Fix and re-test before adding disciplines, jurisdictions, or autonomous actions.
**Exit gate:** measurable pilot acceptance criteria met and accountable owners approve expansion.

## Proposed MVP boundary
Start with project/document control, evidence ledger, RFI/ITP/NCR workflows, source-cited knowledge retrieval, and transparent quantity/BOQ assistance. Keep structural design approval, statutory determinations, and construction authorisation outside autonomous scope.

## Immediate next actions
1. Run and repair the current CI baseline.
2. Audit database lifecycle and consolidate configuration.
3. Define organisation/project/user/role boundaries and add authentication/authorisation.
4. Add migrations and integration tests.
5. Freeze a small MVP acceptance test suite before adding more AI features.

## Current implementation status (starting point)
The repository currently contains a FastAPI foundation, specialist registry, advisory keyword risk triage, SQLite evidence/workflow/standards/document modules, document text extraction, text-only revision diff, and SQLite full-text keyword search. It does not yet provide production authentication, tenant isolation, semantic/vector RAG, scanned-PDF OCR, CAD/drawing geometry comparison, or production deployment. The roadmap above is a plan, not a claim that these capabilities are complete.
