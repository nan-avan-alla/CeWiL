# Architecture Decision Records

## ADR-001: Microservices with monorepo delivery
Status: Accepted.
Target bounded contexts: Identity and Access; Organisation and Project; Document and Evidence; Standards and Knowledge; Engineering Calculation; Construction Workflow; Agent Orchestration; Notification and Reporting.
Each service owns its data and exposes versioned APIs/events. Other services must not write its database. Use REST/OpenAPI for synchronous requests and versioned events for asynchronous work. Design for idempotency, outbox/inbox and compensating workflows; do not assume distributed transactions. Each service needs independent build/test/container, health checks, logs, metrics and traces. Keep one monorepo until boundaries and operational ownership are stable; split deployment units as justified.

## ADR-002: India-first jurisdiction model
Status: Accepted.
Represent country, state/UT, local authority, effective dates, source edition, amendments, project type/use and material/system applicability as structured data. India is the initial market; avoid embedding Indian rules in shared domain logic.

## ADR-003: Engineering governance
Status: Accepted.
LLM output is advisory. Deterministic calculations and source records are separate. Structural adequacy, statutory compliance, inspection disposition and construction authorisation require qualified human review. Preserve inputs, units, assumptions, method version, citations and review state.
