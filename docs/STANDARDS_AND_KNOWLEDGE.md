# Standards registry and source-cited knowledge lookup

## Purpose
The registry records source identity and applicability metadata separately from engineering interpretations. It supports India-first jurisdiction filtering and can represent international sources without pretending that one universal code set applies.

## Source record
A source record stores title, publisher, source type, URL, country, region, locality, code family, edition, amendment, effective/publication dates, access status, verification status, and notes.

## Knowledge entry
A knowledge entry stores a concise, human-entered summary linked to exactly one registered source. Optional applicability fields include jurisdiction, project type, material system, edition, clause, and page. Search responses return citation metadata alongside the entry.

## Verification states
- `unverified`: URL and metadata have not been checked by an authorised reviewer.
- `metadata_checked`: publisher, title, edition and availability metadata checked.
- `reviewed`: the entry's interpretation has been reviewed by an identified qualified reviewer.
- `superseded`: source or edition is no longer current for the stated use.
- `withdrawn`: source is withdrawn or should not be relied upon.

The API does not yet enforce a reviewer role or verify reviewer identity. These labels are workflow metadata only until authentication and approvals are implemented.

## Important limits
`GET /v1/knowledge/search` is a transparent keyword lookup over manually registered summaries. It is not vector search, document ingestion, or semantic RAG. The system does not fetch, parse, or reproduce copyrighted standards. Add only content the organisation is entitled to store and use. A source link alone does not prove that a clause is applicable or current.

Before a design or compliance conclusion, require country, state/province, local authority where relevant, project type/use, material and structural system, adopted edition/amendments, contract hierarchy, and source verification. If these are missing, ask rather than infer.

## Starter official/reference links
The blueprint identifies BIS/NBC, BIS Standards Portal, CPWD, AICTE National Internship Portal, ISO 13822, ASCE/SEI 41, ACI, RICS NRM, buildingSMART, IStructE AI guidance, ISO 17359, and World Bank PPP environmental/social guidance as reference families. Add each actual document/edition as a separate source record after checking the current official catalogue, jurisdiction, licensing, and access terms. Do not treat this list as a verified current code pack.
