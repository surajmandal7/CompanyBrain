# Company Brain Delivery Checklist

- [x] **Secure runtime and deployment foundation** — The application uses server-side project secrets for FalkorDB, Gemini, and admin access; supports the complete database hostname and TLS; never exposes or logs credentials; includes `.env.example`, `.gitignore`, dependency manifests, Dockerfile, and a route manifest; serves the frontend and backend through the managed runtime.

- [x] **FalkorDB graph adapter and safe schema** — The backend verifies database connectivity before reporting health, selects the configured `companyos` graph, uses timeouts and normalized errors, and executes only parameterized/predefined read-only queries for ordinary application operations.

- [x] **Idempotent Nexora sample ingestion** — A protected seed workflow inspects the existing graph, preserves valid records, avoids duplicates, creates the requested 10 employees, 3 teams, 3 projects, 15 tasks, 5 meetings, 5 decisions, 3 policies, documents, source metadata, and meaningful relationships, and reports actual inserted/updated counts without deleting or resetting the graph.

- [x] **FastAPI API surface** — Implement and validate `/api/health`, `/api/dashboard`, `/api/chat`, `/api/projects`, `/api/employees`, `/api/tasks`, `/api/decisions`, and `/api/knowledge-graph`, with safe errors, CORS, request-size limits, and admin protection.

- [x] **Grounded AI assistant** — For each question, the backend routes intent to a safe predefined graph operation, retrieves facts and source records, asks Gemini to synthesize only from the retrieved context, distinguishes insufficient/conflicting information, and returns structured citations that correspond to existing graph records.

- [x] **Enterprise frontend shell** — Provide a responsive dark Company Brain workspace with branding, sidebar navigation, consistent typography, loading states, empty states, useful errors, and pages for Dashboard, AI Assistant, Projects, Employees and Teams, Tasks, Meetings and Decisions, Knowledge Explorer, and Settings.

- [x] **Live dashboard and explorer** — Dashboard metrics and recent activity come from the API in production; Knowledge Explorer visualizes employees, projects, tasks, and decisions and allows node inspection and relationship tracing.

- [x] **Validation and handoff** — Run backend tests for configuration, health/error behavior, safe query routing, citation structure, and idempotent seed helpers; run frontend build/type checks; verify frontend-to-backend integration and Preview readiness; document setup and troubleshooting.

> Publication contract is configured for the managed container runtime. Public release remains a separate checkpoint/publish action.

- [x] **Protected document ingestion** — The Documents page lets an administrator choose multiple TXT, Markdown, JSON, PDF, or DOCX files up to 10 MB each and 50 MB per batch, sends them through a protected multipart endpoint, validates and normalizes JSON server-side, extracts readable text, stores stable checksum-keyed `Document` records and linked `DocumentChunk` records in FalkorDB, reports per-file errors with partial success, lists/searches uploaded sources, and makes uploaded text available to grounded assistant answers with citations.

- [x] **Expanded Nexora graph and multi-node answers** — The idempotent seed now adds 6 teams, 16 employees, 6 projects, 30 tasks, 9 meetings, 9 decisions, 13 source documents, cross-team support, ownership, assignment, dependency, project-decision, and document relationships. Project questions retrieve linked owners, teams, tasks, decisions, and evidence documents; answers are detailed and chat citations identify the exact source document references used.

- [x] **Dense relationship explorer** — The seed adds a second portfolio layer with five teams, 12 people, six projects, 24 tasks, six meetings, six decisions, six documents, cross-project `RELATED_TO` edges, employee collaboration edges, and additional dependencies. The Knowledge Explorer renders Employee, Team, Project, Task, Decision, Meeting, and Document nodes and their relationships.

- [x] **Additional portfolio data and source-aware chat citations** — The seed adds Lighthouse, Horizon, Sentinel, and Mosaic with four teams, eight people, 16 tasks, four meetings, four decisions, four source documents, owners, support teams, dependencies, project links, and collaboration edges. AI Assistant responses now render separate Project and Document citation blocks, including source document titles and `nexora://` references.
