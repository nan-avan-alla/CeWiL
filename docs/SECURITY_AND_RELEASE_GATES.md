# Security and Production Readiness Gates

**Current release classification: Development only — not approved for public or confidential project use.**

This is a blocking release checklist, not a claim that controls are implemented.

## Trust boundaries and assets
- Organisation and project records.
- Drawings, specifications, BOQs, inspection records and uploaded evidence.
- Standards metadata, source documents, citations and review states.
- Engineering calculations, assumptions, units, outputs and approvals.
- User identities, credentials, access tokens and audit history.

## Required controls before any external pilot

### Identity and authorisation
- [ ] Use a maintained identity provider (OIDC/OAuth2); caller-supplied actor labels are not identity.
- [ ] Enforce organisation membership and project membership on every read and write.
- [ ] Define least-privilege roles; separate reviewer, engineer, project manager and administrator capabilities.
- [ ] Deny by default; test cross-tenant and cross-project IDOR cases.
- [ ] Rotate/revoke sessions and credentials; protect secrets outside source control.

### Upload and document handling
- [ ] Enforce file size, extension, MIME and content-signature checks.
- [ ] Quarantine uploads until malware scanning succeeds; reject unsupported archives and active content.
- [ ] Store uploads outside the web root with opaque object keys and tenant/project access checks.
- [ ] Apply retention, deletion, legal hold and audit policies.
- [ ] Treat extracted text as untrusted input; document content must never grant tool authority.

### Data and platform
- [ ] Replace SQLite as the production multi-user database; use managed relational storage with migrations and least-privilege credentials.
- [ ] Encrypt transport and storage; define key management and rotation.
- [ ] Add rate limits, request size limits, secure headers, CORS allowlists and dependency/security scanning.
- [ ] Add structured logs, metrics, traces, alerting and privacy-safe audit events.
- [ ] Verify automated backups with restore drills and documented RPO/RTO.
- [ ] Add deployment rollback, health/readiness probes and incident response procedures.

### Engineering governance
- [ ] Keep calculations deterministic, versioned and reproducible with inputs, units, assumptions and method version.
- [ ] Bind knowledge claims to authoritative source edition, jurisdiction, effective date and clause/page citations.
- [ ] Do not present keyword search or unreviewed knowledge as verified code compliance.
- [ ] Require qualified human approval for structural adequacy, statutory compliance, inspection disposition and construction authorisation.
- [ ] Record reviewer identity, role, decision, timestamp and evidence snapshot.

## Minimum release acceptance tests
1. Anonymous requests to protected APIs are rejected.
2. A user cannot list, fetch, search, diff, update or delete another project's resources by guessing IDs.
3. A user from one organisation cannot access another organisation's data.
4. Revoked users and credentials lose access within the documented revocation window.
5. Uploads with mismatched MIME/signature, oversized content and malware fixtures are quarantined or rejected.
6. Every privileged action creates an immutable, attributable audit event.
7. A backup can be restored into an isolated environment and integrity-checked.
8. A failed release can be rolled back without corrupting evidence or workflow history.
9. Engineering outputs remain drafts until an authorised qualified reviewer approves them.

## Current known limitations
The current API accepts caller-supplied project IDs and actor labels and has no authentication or project membership enforcement. SQLite modules are not a production multi-tenant persistence layer. Upload quarantine/malware scanning, immutable audit trail, backup/restore automation and deployment rollback are not implemented. Do not expose the service publicly or upload confidential project material.
