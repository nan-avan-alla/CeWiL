# Container Runbook

This container is a repeatable **local development** packaging option. It is not a production deployment profile.

## Build and run

```bash
docker build -t cewil-engineering-os:dev .
docker run --rm -p 8000:8000 \
  -v cewil-data:/app/data \
  cewil-engineering-os:dev
```

Open `http://localhost:8000/docs` for the API schema and `http://localhost:8000/health` for the process health check.

The container runs as a non-root user. The named volume persists the SQLite database and document files across container replacement.

## Configuration

- `CEWIL_DB_PATH`: SQLite database path (default `/app/data/cewil.db`).
- `CEWIL_DOCUMENTS_PATH`: document storage path (default `/app/data/documents`).

Do not mount confidential project data or expose this API to an untrusted network. The current application does not enforce authenticated identity, project membership, tenant isolation, upload malware quarantine, or production-grade persistence. A non-root container and health check do not resolve those gaps.

## Before any external pilot

Complete every applicable gate in [Security and Production Readiness Gates](SECURITY_AND_RELEASE_GATES.md), including OIDC integration, server-enforced project authorisation, production database migrations, object storage, malware scanning, immutable audit, backup/restore tests, monitoring, and rollback. The container must not be promoted as production-ready until those controls are implemented and independently verified.
