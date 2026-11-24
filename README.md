# CeWiL Engineering Operating System

A governed engineering workflow platform foundation for civil-engineering practice.

## Scope of this initial repository foundation
- Ten specialist workflow domains with a central routing registry.
- FastAPI service exposing health, agent catalogue, and routing endpoints.
- Explicit human-review gates for safety-critical engineering decisions.
- Deterministic quantity utilities for simple unit conversions and concrete volume.
- Pytest checks and GitHub Actions CI.

## Specialist domains
1. Civil Engineering Practice Workflow
2. Construction Execution and Quality Control
3. Structural Design (RC and Steel)
4. Building Estimation, BOQ, Rate Analysis
5. Construction Approvals and Municipal Compliance
6. Structural Auditing of Existing Buildings
7. On-site Concrete Strength and Construction-Practice Guidance
8. Structural Health Monitoring
9. Civil Engineering Student Internship Mentoring
10. Final-Year Civil Engineering Project Assistance

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn cewil_os.main:app --reload
```

## Safety boundary
This is a software foundation, not an engineering authority or certification system. Outputs affecting structural safety, code compliance, construction execution, or public safety require qualified professional review. No autonomous approval, sign-off, or construction instruction is provided.

## Current limitations
No production database, authentication, document OCR, jurisdiction-specific code corpus, external LLM, cloud infrastructure, or persistent evidence ledger is connected in this initial foundation. These require explicit design, validation, and deployment work.
