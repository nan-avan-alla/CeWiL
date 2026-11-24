# Platform services: evidence, workflow, and risk triage

This increment implements the shared P0 foundation described in the CeWiL architecture blueprint.

## Evidence ledger
Each evidence record is associated with a project and captures evidence type, title, source reference, revision, description, recorder, timestamp, and structured metadata. Evidence records are not proof of engineering correctness; they preserve traceability for later review.

## Workflow service
The workflow register supports RFI, ITP, NCR, submittal, inspection, and action records. Status transitions are constrained:
- open -> in_review, blocked, closed
- in_review -> open, blocked, closed
- blocked -> open, in_review
- closed -> terminal

Every transition records actor text, timestamp, and note. Actor identity is not authenticated in this increment; do not treat it as a verified signature or approval.

## Risk triage
A conservative keyword heuristic raises review priority for selected structural, life-safety, concrete, and statutory topics. It is intentionally transparent and must be treated as a routing hint only. It is not validated against a professional risk dataset and does not replace an engineer's assessment.

## Remaining P0 controls
Authentication and role-based authorisation, tenant isolation, source registry with edition/amendment metadata, RAG with clause-level citations, document ingestion and revision detection, reviewer identity verification, durable audit integrity, and expert-reviewed evaluation datasets remain unimplemented.
