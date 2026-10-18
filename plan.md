# Company Brain — Implementation Plan

## Scope and approach

Company Brain is a full-stack enterprise knowledge assistant for Nexora Technologies. The project uses a single FastAPI runtime on port 3000 that serves the compiled React/Vite frontend and exposes REST endpoints under `/api`. FalkorDB Cloud is the system of record for company knowledge; Google Gemini is used only from the server for intent classification and grounded answer synthesis. No database credentials or model keys enter browser code.

The backend is deliberately modular: configuration and redacted health checks, a FalkorDB adapter with TLS and query timeouts, schema/seed data, read-only graph operations, source attribution, Gemini orchestration with a strict operation allowlist, and FastAPI routes. The admin seed endpoint is protected by `ADMIN_API_KEY`; ordinary chat is read-only and never executes model-generated Cypher.

The frontend is a dark, responsive SaaS workspace with an asymmetric command-center layout: a persistent rail, a wide working canvas, and a right-side signal panel on dashboard views. It uses live REST data, skeleton/loading states, empty/error states, and a compact force-graph-like SVG explorer fed by `/api/knowledge-graph`. The AI Assistant uses a real chat endpoint and renders structured citations.

## Project structure

- `server/main.py` — FastAPI app, API routes, static serving, CORS, request validation.
- `server/config.py` — environment parsing and safe configuration validation.
- `server/db.py` — FalkorDB Cloud TLS adapter and normalized query results.
- `server/graph_queries.py` — predefined read-only graph operations, composite project context retrieval, and dashboard aggregations.
- `server/seed_data.py` — idempotent Nexora sample graph data across multiple connected portfolio layers and admin seed workflow.
- `server/ai_agent.py` — deterministic safe routing for strong project signals, multi-node grounded context assembly, detailed answer generation, and source-document citations.
- `server/prompts.py` — prompt templates and safety constraints.
- `server/document_ingest.py` — server-side TXT/Markdown/PDF/DOCX extraction, checksum IDs, and chunk upserts.
- `frontend/src/` — React application, navigation, pages, API client, dense multi-label graph explorer, and source-aware assistant UI with separate project/document citations.
- `public/manus-routes.json` — route manifest for Preview/publishing.
- `Dockerfile` — production image that builds frontend and runs FastAPI.

## Design direction

Three possible directions were considered: **Signal Noir** (0.07): editorial command center with ink-black surfaces and electric lime signals; **Quiet Ledger** (0.05): calm slate workspace with blue-gray hierarchy; **Orbit Ops** (0.08): deep navy operations console with violet highlights. The selected direction is **Signal Noir**.

### Design Movement
Signal Noir: a restrained enterprise command center influenced by Swiss editorial systems and observability consoles.

### Core Principles
1. Make the graph legible: relationships, ownership, and evidence are always close to the surface.
2. Use contrast as hierarchy: warm-white type, graphite surfaces, and one electric signal color.
3. Prefer compact, information-dense modules over decorative dashboards.
4. Every AI answer should feel inspectable, not magical.

### Color Philosophy
Graphite and near-black establish focus; soft parchment text prevents the dark UI from feeling cold; acid chartreuse marks live signals, selected states, and calls to action; cyan and amber are reserved for data semantics such as verified context and risk.

### Layout Paradigm
A left rail frames an editorial canvas. Dashboard pages use a broad primary column for the main narrative and a narrow signal column for recent activity, instead of a symmetrical card grid. Tables and chat use full-width reading lanes with strong left alignment.

### Signature Elements
- A small lime “pulse” mark in the wordmark and active navigation.
- Hairline dividers and indexed labels such as `01 / SIGNALS`.
- Citation chips that expose provenance as first-class UI, not footnotes.

### Interaction Philosophy
Interactions should feel like tracing a thread through a company: clicking a project filters its related tasks, a citation opens its record context, and node selection in the explorer updates the inspector. Optimistic styling is avoided for data writes; actions show explicit pending and result states.

### Animation
Use 160–220ms ease-out transitions for rail expansion, tabs, and cards. Use a slow 3.5s pulse on live signal dots, and a subtle 900ms graph line draw when the explorer first mounts. Avoid looping decorative motion.

### Typography System
Use `Inter` for UI and `Space Grotesk` for display labels via CSS imports, with system fallbacks. Headings are tight and medium-weight; labels are uppercase, letter-spaced, and small; body copy stays at 14–16px with generous line height.

### Brand Essence
The company’s memory, connected and queryable. Personality: precise, calm, traceable.

### Brand Voice
Headlines are concise and operational. CTAs are direct and evidence-oriented. Example lines: “Trace the decision.” and “Ask the graph, not a guess.”

### Wordmark & Logo
A compact three-node monogram: three rounded points connected in a triangular loop, followed by “company brain”. The mark is rendered in CSS/SVG so it remains crisp at any size.

### Signature Brand Color
Signal lime `#C7F36A`, used sparingly enough to remain ownable and meaningful.

## Build and delivery workflow

1. Install pinned frontend and Python dependencies.
2. Implement configuration, FalkorDB adapter, graph operations, seed data, and AI agent.
3. Implement the React shell and all required pages with REST integration.
4. Add the protected Documents page and multipart upload endpoint; extract supported files server-side, store `Document` and `DocumentChunk` records in FalkorDB, and expose uploaded content to grounded retrieval.
5. Run static checks, backend unit tests, upload smoke tests, and a local Preview smoke test.
6. Configure container build and published routing for `/api/*` to the server and SPA fallback for frontend routes.
7. Commit and push the completed implementation to the managed `main` branch for a checkpoint.

The initial delivery does not automatically seed or mutate the configured graph. The Settings page exposes a protected seed action that reports inserted/updated counts and preserves existing valid records.
