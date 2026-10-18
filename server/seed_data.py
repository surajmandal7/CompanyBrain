from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .db import FalkorDB


@dataclass(frozen=True)
class Record:
    label: str
    id: str
    props: dict[str, Any]


TEAMS = [
    Record("Team", "team-product", {"name": "Product & Design", "description": "Product strategy, research, and design."}),
    Record("Team", "team-engineering", {"name": "Engineering", "description": "Platform and product engineering."}),
    Record("Team", "team-growth", {"name": "Growth & Customer", "description": "Go-to-market and customer outcomes."}),
]

EMPLOYEES = [
    Record("Employee", "emp-rahul", {"name": "Rahul Sharma", "role": "VP Product", "email": "rahul@nexora.example", "location": "Bengaluru"}),
    Record("Employee", "emp-maya", {"name": "Maya Chen", "role": "Engineering Manager", "email": "maya@nexora.example", "location": "Singapore"}),
    Record("Employee", "emp-lena", {"name": "Lena Ortiz", "role": "Staff Designer", "email": "lena@nexora.example", "location": "Madrid"}),
    Record("Employee", "emp-owen", {"name": "Owen Brooks", "role": "Senior Engineer", "email": "owen@nexora.example", "location": "London"}),
    Record("Employee", "emp-priya", {"name": "Priya Nair", "role": "Product Manager", "email": "priya@nexora.example", "location": "Bengaluru"}),
    Record("Employee", "emp-daniel", {"name": "Daniel Kim", "role": "Data Lead", "email": "daniel@nexora.example", "location": "Seoul"}),
    Record("Employee", "emp-sofia", {"name": "Sofia Alvarez", "role": "Customer Success Lead", "email": "sofia@nexora.example", "location": "Austin"}),
    Record("Employee", "emp-nikhil", {"name": "Nikhil Rao", "role": "Growth Manager", "email": "nikhil@nexora.example", "location": "Mumbai"}),
    Record("Employee", "emp-amara", {"name": "Amara Okafor", "role": "Security Engineer", "email": "amara@nexora.example", "location": "Dublin"}),
    Record("Employee", "emp-jules", {"name": "Jules Martin", "role": "Finance Partner", "email": "jules@nexora.example", "location": "Paris"}),
]

PROJECTS = [
    Record("Project", "proj-phoenix", {"name": "Project Phoenix", "status": "In Flight", "priority": "P0", "description": "Rebuild the core workspace around connected company knowledge.", "dueDate": "2026-11-20"}),
    Record("Project", "proj-atlas", {"name": "Project Atlas", "status": "At Risk", "priority": "P1", "description": "Customer-facing analytics for account teams.", "dueDate": "2026-10-31"}),
    Record("Project", "proj-orion", {"name": "Project Orion", "status": "Planning", "priority": "P1", "description": "A privacy-first search experience for regulated customers.", "dueDate": "2027-01-15"}),
]

TASKS = [
    ("task-phoenix-schema", "Define knowledge graph schema", "Done", "P0", "2026-09-15", "emp-priya", "proj-phoenix"),
    ("task-phoenix-ingest", "Implement source ingestion", "In Progress", "P0", "2026-10-28", "emp-owen", "proj-phoenix"),
    ("task-phoenix-permissions", "Review workspace permissions", "Blocked", "P0", "2026-10-24", "emp-amara", "proj-phoenix"),
    ("task-phoenix-assistant", "Ground assistant answers", "In Progress", "P0", "2026-11-05", "emp-maya", "proj-phoenix"),
    ("task-phoenix-explorer", "Ship graph explorer", "Open", "P1", "2026-11-12", "emp-lena", "proj-phoenix"),
    ("task-atlas-events", "Instrument account events", "In Progress", "P1", "2026-10-18", "emp-daniel", "proj-atlas"),
    ("task-atlas-dashboard", "Build retention dashboard", "Blocked", "P1", "2026-10-22", "emp-owen", "proj-atlas"),
    ("task-atlas-research", "Interview top accounts", "Done", "P1", "2026-09-30", "emp-sofia", "proj-atlas"),
    ("task-atlas-alerts", "Define risk alerts", "Open", "P2", "2026-10-29", "emp-nikhil", "proj-atlas"),
    ("task-atlas-qa", "Validate cohort metrics", "Open", "P1", "2026-10-30", "emp-daniel", "proj-atlas"),
    ("task-orion-threat", "Complete threat model", "In Progress", "P0", "2026-12-03", "emp-amara", "proj-orion"),
    ("task-orion-prototype", "Prototype policy search", "Open", "P1", "2026-12-15", "emp-lena", "proj-orion"),
    ("task-orion-pricing", "Model enterprise pricing", "Open", "P2", "2026-12-12", "emp-jules", "proj-orion"),
    ("task-orion-beta", "Recruit design partners", "Open", "P1", "2027-01-05", "emp-sofia", "proj-orion"),
    ("task-orion-legal", "Review regional retention rules", "Blocked", "P0", "2026-12-08", "emp-jules", "proj-orion"),
]

MEETINGS = [
    Record("Meeting", "meeting-101", {"title": "Phoenix kickoff", "date": "2026-09-08", "summary": "Aligned on graph-first architecture and a November launch target."}),
    Record("Meeting", "meeting-102", {"title": "Atlas metrics review", "date": "2026-09-22", "summary": "Found inconsistent cohort definitions across customer teams."}),
    Record("Meeting", "meeting-103", {"title": "Security council", "date": "2026-10-02", "summary": "Reviewed permission boundaries and regional retention requirements."}),
    Record("Meeting", "meeting-104", {"title": "October operating review", "date": "2026-10-10", "summary": "Moved Atlas to at-risk while instrumentation catches up."}),
    Record("Meeting", "meeting-105", {"title": "Product council", "date": "2026-10-15", "summary": "Confirmed Phoenix ownership and assistant grounding principles."}),
]

DECISIONS = [
    Record("Decision", "decision-201", {"title": "Make Phoenix the first graph-backed workspace", "date": "2026-09-08", "status": "Active", "reason": "A focused first surface gives teams one reliable place to test connected knowledge."}),
    Record("Decision", "decision-202", {"title": "Standardize cohort definitions before Atlas launch", "date": "2026-09-22", "status": "Active", "reason": "Comparable metrics are required before account teams can trust the dashboard."}),
    Record("Decision", "decision-203", {"title": "Use least-privilege access for graph sources", "date": "2026-10-02", "status": "Active", "reason": "Company knowledge should be useful without widening access to sensitive source systems."}),
    Record("Decision", "decision-204", {"title": "Move Atlas to at-risk", "date": "2026-10-10", "status": "Active", "reason": "Missing instrumentation puts the committed reporting milestone at risk."}),
    Record("Decision", "decision-205", {"title": "Require citations in assistant answers", "date": "2026-10-15", "status": "Active", "reason": "Employees need to trace every answer back to a real company record."}),
]

DOCUMENTS = [
    Record("Document", "doc-phoenix", {"title": "Phoenix product brief", "sourceType": "Product brief", "sourceRef": "nexora://docs/phoenix-brief", "summary": "Phoenix is the first graph-backed workspace, with a November launch target and grounded assistant requirements."}),
    Record("Document", "doc-security", {"title": "Security council notes", "sourceType": "Meeting notes", "sourceRef": "nexora://meetings/security-council", "summary": "Security review covers least-privilege access, permission boundaries, and regional retention requirements."}),
    Record("Document", "doc-leave", {"title": "Nexora leave handbook", "sourceType": "Policy handbook", "sourceRef": "nexora://policies/leave", "summary": "Employees receive 24 annual paid leave days and should request manager approval five business days ahead when possible."}),
]

POLICIES = [
    Record("Policy", "policy-leave", {"name": "Company leave policy", "summary": "Employees receive 24 annual paid leave days, with manager approval requested at least five business days ahead when possible.", "updatedAt": "2026-01-12"}),
    Record("Policy", "policy-security", {"name": "Information security policy", "summary": "Sensitive customer and employee data must be accessed on a least-privilege basis and never copied into unapproved tools.", "updatedAt": "2026-02-05"}),
    Record("Policy", "policy-remote", {"name": "Remote work policy", "summary": "Teams may work remotely with a shared overlap window and quarterly in-person planning for distributed groups.", "updatedAt": "2026-03-18"}),
]

MORE_TEAMS = [
    Record("Team", "team-research", {"name": "Research & Insights", "description": "Customer research, measurement, and decision intelligence."}),
    Record("Team", "team-platform", {"name": "Platform Infrastructure", "description": "Reliability, data foundations, and internal developer systems."}),
    Record("Team", "team-operations", {"name": "Customer Operations", "description": "Implementation, support operations, and customer enablement."}),
]

MORE_EMPLOYEES = [
    Record("Employee", "emp-aisha", {"name": "Aisha Williams", "role": "Research Director", "email": "aisha@nexora.example", "location": "New York"}),
    Record("Employee", "emp-victor", {"name": "Victor Petrov", "role": "Platform Lead", "email": "victor@nexora.example", "location": "Warsaw"}),
    Record("Employee", "emp-marcus", {"name": "Marcus Lee", "role": "Operations Director", "email": "marcus@nexora.example", "location": "Toronto"}),
    Record("Employee", "emp-elena", {"name": "Elena Rossi", "role": "Analytics Engineer", "email": "elena@nexora.example", "location": "Milan"}),
    Record("Employee", "emp-tomas", {"name": "Tomás Silva", "role": "Solutions Architect", "email": "tomas@nexora.example", "location": "Lisbon"}),
    Record("Employee", "emp-grace", {"name": "Grace Mensah", "role": "Customer Enablement Manager", "email": "grace@nexora.example", "location": "Accra"}),
]

MORE_PROJECTS = [
    Record("Project", "proj-nova", {"name": "Project Nova", "status": "In Flight", "priority": "P1", "description": "Unify product telemetry and customer health signals for proactive decisions.", "dueDate": "2026-12-12"}),
    Record("Project", "proj-helix", {"name": "Project Helix", "status": "At Risk", "priority": "P1", "description": "Standardize customer onboarding and implementation playbooks.", "dueDate": "2026-11-05"}),
    Record("Project", "proj-cedar", {"name": "Project Cedar", "status": "Discovery", "priority": "P2", "description": "Create a repeatable research program for enterprise product signals.", "dueDate": "2027-02-18"}),
]

MORE_TASKS = [
    ("task-nova-pipeline", "Consolidate telemetry pipelines", "In Progress", "P1", "2026-11-15", "emp-victor", "proj-nova"),
    ("task-nova-health", "Define customer health score", "In Progress", "P1", "2026-11-22", "emp-elena", "proj-nova"),
    ("task-nova-governance", "Approve telemetry governance", "Blocked", "P0", "2026-11-08", "emp-amara", "proj-nova"),
    ("task-nova-alerts", "Prototype health alerts", "Open", "P2", "2026-12-01", "emp-daniel", "proj-nova"),
    ("task-nova-rollout", "Pilot Nova with account teams", "Open", "P1", "2026-12-08", "emp-sofia", "proj-nova"),
    ("task-helix-playbook", "Write onboarding playbook", "In Progress", "P1", "2026-10-25", "emp-grace", "proj-helix"),
    ("task-helix-training", "Run implementation training", "Open", "P1", "2026-10-30", "emp-tomas", "proj-helix"),
    ("task-helix-roles", "Map customer handoff roles", "Blocked", "P1", "2026-10-28", "emp-marcus", "proj-helix"),
    ("task-helix-sla", "Review onboarding SLA", "Done", "P2", "2026-10-12", "emp-jules", "proj-helix"),
    ("task-helix-pilot", "Select pilot customers", "Done", "P1", "2026-10-05", "emp-sofia", "proj-helix"),
    ("task-cedar-interviews", "Complete enterprise interviews", "In Progress", "P1", "2027-01-12", "emp-aisha", "proj-cedar"),
    ("task-cedar-taxonomy", "Create research signal taxonomy", "Open", "P2", "2027-01-26", "emp-lena", "proj-cedar"),
    ("task-cedar-consent", "Approve research consent language", "Blocked", "P0", "2027-01-08", "emp-amara", "proj-cedar"),
    ("task-cedar-synthesis", "Synthesize top customer themes", "Open", "P1", "2027-02-02", "emp-aisha", "proj-cedar"),
    ("task-cedar-readout", "Prepare executive research readout", "Open", "P2", "2027-02-12", "emp-rahul", "proj-cedar"),
]

MORE_MEETINGS = [
    Record("Meeting", "meeting-106", {"title": "Nova architecture review", "date": "2026-10-06", "summary": "Agreed to consolidate telemetry before defining customer health scoring."}),
    Record("Meeting", "meeting-107", {"title": "Customer operations forum", "date": "2026-10-09", "summary": "Identified unclear ownership at the handoff between implementation and support."}),
    Record("Meeting", "meeting-108", {"title": "Research planning session", "date": "2026-10-13", "summary": "Prioritized enterprise interviews and a shared signal taxonomy for Cedar."}),
    Record("Meeting", "meeting-109", {"title": "Portfolio review", "date": "2026-10-16", "summary": "Kept Nova in flight, Helix at risk, and Cedar in discovery pending consent approval."}),
]

MORE_DECISIONS = [
    Record("Decision", "decision-206", {"title": "Consolidate telemetry before health scoring", "date": "2026-10-06", "status": "Active", "reason": "A single event vocabulary is required before customer health scores can be trusted across products."}),
    Record("Decision", "decision-207", {"title": "Create one accountable owner for customer handoffs", "date": "2026-10-09", "status": "At Risk", "reason": "Unclear responsibility at the implementation-to-support handoff is creating inconsistent customer experiences."}),
    Record("Decision", "decision-208", {"title": "Use enterprise interviews as Cedar's first evidence set", "date": "2026-10-13", "status": "Active", "reason": "Direct customer evidence will anchor the research taxonomy before broader survey work."}),
    Record("Decision", "decision-209", {"title": "Keep Helix at risk until role mapping is complete", "date": "2026-10-16", "status": "Active", "reason": "The program can meet its date only if ownership is explicit at every onboarding transition."}),
]

MORE_DOCUMENTS = [
    Record("Document", "doc-atlas-metrics", {"title": "Atlas metrics review", "sourceType": "Meeting notes", "sourceRef": "nexora://meetings/atlas-metrics", "summary": "Atlas needs standardized cohort definitions and event instrumentation before launch."}),
    Record("Document", "doc-orion-threat", {"title": "Orion threat model", "sourceType": "Security review", "sourceRef": "nexora://security/orion-threat-model", "summary": "Orion's regional retention and least-privilege controls remain launch-critical."}),
    Record("Document", "doc-nova-charter", {"title": "Nova program charter", "sourceType": "Program charter", "sourceRef": "nexora://projects/nova-charter", "summary": "Nova consolidates telemetry and defines the customer health signal contract."}),
    Record("Document", "doc-helix-playbook", {"title": "Helix onboarding playbook", "sourceType": "Operations playbook", "sourceRef": "nexora://projects/helix-playbook", "summary": "Helix standardizes implementation, handoff, and customer enablement responsibilities."}),
    Record("Document", "doc-cedar-research", {"title": "Cedar research plan", "sourceType": "Research plan", "sourceRef": "nexora://projects/cedar-research", "summary": "Cedar begins with enterprise interviews and a shared taxonomy of customer signals."}),
]

DENSE_TEAMS = [
    Record("Team", "team-ai", {"name": "AI & Automation", "description": "Applied intelligence, evaluation, and workflow automation."}),
    Record("Team", "team-reliability", {"name": "Reliability Engineering", "description": "Observability, incident response, and platform resilience."}),
    Record("Team", "team-legal", {"name": "Legal & Compliance", "description": "Privacy, contracts, governance, and regulatory readiness."}),
    Record("Team", "team-partnerships", {"name": "Strategic Partnerships", "description": "Platform alliances, integrations, and ecosystem growth."}),
    Record("Team", "team-finance", {"name": "Finance & Planning", "description": "Planning, pricing, forecasting, and investment decisions."}),
]

DENSE_EMPLOYEES = [
    Record("Employee", "emp-hiro", {"name": "Hiro Tanaka", "role": "ML Platform Manager", "email": "hiro@nexora.example", "location": "Tokyo"}),
    Record("Employee", "emp-becca", {"name": "Becca Stone", "role": "Site Reliability Engineer", "email": "becca@nexora.example", "location": "Denver"}),
    Record("Employee", "emp-samir", {"name": "Samir Haddad", "role": "Privacy Counsel", "email": "samir@nexora.example", "location": "Dubai"}),
    Record("Employee", "emp-nina", {"name": "Nina Petrescu", "role": "Partnerships Lead", "email": "nina@nexora.example", "location": "Bucharest"}),
    Record("Employee", "emp-diego", {"name": "Diego Morales", "role": "FP&A Manager", "email": "diego@nexora.example", "location": "Mexico City"}),
    Record("Employee", "emp-mei", {"name": "Mei Wong", "role": "Product Operations Lead", "email": "mei@nexora.example", "location": "Hong Kong"}),
    Record("Employee", "emp-arjun", {"name": "Arjun Patel", "role": "Machine Learning Engineer", "email": "arjun@nexora.example", "location": "Pune"}),
    Record("Employee", "emp-fatima", {"name": "Fatima Zahra", "role": "Compliance Analyst", "email": "fatima@nexora.example", "location": "Casablanca"}),
    Record("Employee", "emp-chloe", {"name": "Chloe Bennett", "role": "Integration Engineer", "email": "chloe@nexora.example", "location": "Dublin"}),
    Record("Employee", "emp-ben", {"name": "Ben Carter", "role": "Solutions Consultant", "email": "ben@nexora.example", "location": "Chicago"}),
    Record("Employee", "emp-lucia", {"name": "Lucia Bianchi", "role": "Senior Financial Analyst", "email": "lucia@nexora.example", "location": "Rome"}),
    Record("Employee", "emp-noah", {"name": "Noah Williams", "role": "Incident Commander", "email": "noah@nexora.example", "location": "Atlanta"}),
]

DENSE_PROJECTS = [
    Record("Project", "proj-polaris", {"name": "Project Polaris", "status": "In Flight", "priority": "P0", "description": "Build a governed evaluation platform for AI-powered company workflows.", "dueDate": "2027-01-22"}),
    Record("Project", "proj-meridian", {"name": "Project Meridian", "status": "At Risk", "priority": "P1", "description": "Launch a resilient integration layer for strategic platform partners.", "dueDate": "2026-12-19"}),
    Record("Project", "proj-ember", {"name": "Project Ember", "status": "Planning", "priority": "P2", "description": "Modernize financial planning with scenario-based forecasting.", "dueDate": "2027-02-05"}),
    Record("Project", "proj-quill", {"name": "Project Quill", "status": "In Flight", "priority": "P1", "description": "Create a governed contract and policy knowledge layer.", "dueDate": "2027-01-12"}),
    Record("Project", "proj-solstice", {"name": "Project Solstice", "status": "Discovery", "priority": "P2", "description": "Design a unified incident learning and reliability analytics program.", "dueDate": "2027-03-10"}),
    Record("Project", "proj-vela", {"name": "Project Vela", "status": "On Hold", "priority": "P1", "description": "Explore a partner marketplace for reusable Nexora extensions.", "dueDate": "2027-04-16"}),
]

DENSE_TASKS = [
    ("task-polaris-eval", "Define AI evaluation rubric", "In Progress", "P0", "2026-12-04", "emp-hiro", "proj-polaris"),
    ("task-polaris-datasets", "Curate grounded evaluation sets", "In Progress", "P0", "2026-12-12", "emp-arjun", "proj-polaris"),
    ("task-polaris-risk", "Review model risk controls", "Blocked", "P0", "2026-12-18", "emp-samir", "proj-polaris"),
    ("task-polaris-console", "Build evaluator console", "Open", "P1", "2027-01-08", "emp-maya", "proj-polaris"),
    ("task-meridian-contract", "Finalize partner API contract", "In Progress", "P1", "2026-11-21", "emp-chloe", "proj-meridian"),
    ("task-meridian-retries", "Implement retry and replay queue", "Blocked", "P0", "2026-11-29", "emp-becca", "proj-meridian"),
    ("task-meridian-cert", "Complete partner certification", "Open", "P1", "2026-12-05", "emp-nina", "proj-meridian"),
    ("task-meridian-pilot", "Select integration pilot", "Done", "P1", "2026-11-10", "emp-ben", "proj-meridian"),
    ("task-ember-model", "Create planning scenario model", "In Progress", "P2", "2027-01-09", "emp-diego", "proj-ember"),
    ("task-ember-inputs", "Map forecast inputs", "Open", "P2", "2027-01-15", "emp-lucia", "proj-ember"),
    ("task-ember-approvals", "Define planning approval flow", "Blocked", "P1", "2027-01-20", "emp-mei", "proj-ember"),
    ("task-ember-pilot", "Run finance pilot", "Open", "P2", "2027-01-28", "emp-diego", "proj-ember"),
    ("task-quill-taxonomy", "Create contract taxonomy", "In Progress", "P1", "2026-12-15", "emp-fatima", "proj-quill"),
    ("task-quill-ingest", "Ingest approved agreements", "Open", "P1", "2026-12-22", "emp-chloe", "proj-quill"),
    ("task-quill-retention", "Validate retention schedule", "Blocked", "P0", "2027-01-03", "emp-samir", "proj-quill"),
    ("task-quill-search", "Prototype policy search", "Open", "P1", "2027-01-07", "emp-arjun", "proj-quill"),
    ("task-solstice-signals", "Define incident learning signals", "In Progress", "P2", "2027-02-04", "emp-noah", "proj-solstice"),
    ("task-solstice-retro", "Standardize incident retrospectives", "Open", "P2", "2027-02-12", "emp-becca", "proj-solstice"),
    ("task-solstice-dashboard", "Build reliability dashboard", "Open", "P2", "2027-02-20", "emp-daniel", "proj-solstice"),
    ("task-solstice-pilot", "Choose service pilot", "Done", "P2", "2027-01-31", "emp-noah", "proj-solstice"),
    ("task-vela-discovery", "Interview ecosystem partners", "Open", "P2", "2027-03-05", "emp-nina", "proj-vela"),
    ("task-vela-economics", "Model marketplace economics", "Open", "P1", "2027-03-18", "emp-lucia", "proj-vela"),
    ("task-vela-controls", "Define extension review controls", "Blocked", "P1", "2027-03-25", "emp-fatima", "proj-vela"),
    ("task-vela-thesis", "Write investment thesis", "Open", "P2", "2027-04-02", "emp-mei", "proj-vela"),
]

DENSE_MEETINGS = [
    Record("Meeting", "meeting-110", {"title": "Polaris model governance review", "date": "2026-10-20", "summary": "Aligned on evaluation sets, rubric ownership, and the need for model risk sign-off."}),
    Record("Meeting", "meeting-111", {"title": "Meridian partner readiness", "date": "2026-10-22", "summary": "Found retry queue gaps that threaten the partner certification milestone."}),
    Record("Meeting", "meeting-112", {"title": "Finance planning workshop", "date": "2026-10-24", "summary": "Prioritized scenario modeling and clarified approval dependencies for Ember."}),
    Record("Meeting", "meeting-113", {"title": "Policy knowledge working group", "date": "2026-10-27", "summary": "Agreed on contract taxonomy and retention validation as Quill launch gates."}),
    Record("Meeting", "meeting-114", {"title": "Reliability learning forum", "date": "2026-10-29", "summary": "Selected incident learning signals and a first service pilot for Solstice."}),
    Record("Meeting", "meeting-115", {"title": "Ecosystem strategy review", "date": "2026-11-01", "summary": "Paused Vela until partner economics and extension review controls are clearer."}),
]

DENSE_DECISIONS = [
    Record("Decision", "decision-210", {"title": "Require human sign-off for AI risk controls", "date": "2026-10-20", "status": "Active", "reason": "Evaluation evidence alone is not sufficient for high-impact workflow releases."}),
    Record("Decision", "decision-211", {"title": "Hold Meridian certification until replay works", "date": "2026-10-22", "status": "At Risk", "reason": "Partners need deterministic recovery when events arrive out of order or after an outage."}),
    Record("Decision", "decision-212", {"title": "Use scenario planning for the next finance cycle", "date": "2026-10-24", "status": "Active", "reason": "Scenario comparisons will make investment trade-offs explicit before annual planning."}),
    Record("Decision", "decision-213", {"title": "Make retention validation a Quill launch gate", "date": "2026-10-27", "status": "Active", "reason": "Contract knowledge must respect regional retention requirements before broader search access."}),
    Record("Decision", "decision-214", {"title": "Start Solstice with incident learning signals", "date": "2026-10-29", "status": "Active", "reason": "A small, consistent signal set will make reliability learning measurable across services."}),
    Record("Decision", "decision-215", {"title": "Pause Vela pending marketplace controls", "date": "2026-11-01", "status": "On Hold", "reason": "Partner growth should not outpace extension review, economics, and compliance controls."}),
]

DENSE_DOCUMENTS = [
    Record("Document", "doc-polaris-governance", {"title": "Polaris governance memo", "sourceType": "Governance memo", "sourceRef": "nexora://projects/polaris-governance", "summary": "Polaris requires evaluation evidence and human sign-off for high-impact AI workflows."}),
    Record("Document", "doc-meridian-readiness", {"title": "Meridian partner readiness", "sourceType": "Partner review", "sourceRef": "nexora://projects/meridian-readiness", "summary": "Meridian certification is gated by deterministic retry and replay behavior."}),
    Record("Document", "doc-ember-plan", {"title": "Ember planning brief", "sourceType": "Planning brief", "sourceRef": "nexora://projects/ember-plan", "summary": "Ember uses scenario-based financial planning with an explicit approval flow."}),
    Record("Document", "doc-quill-controls", {"title": "Quill policy controls", "sourceType": "Compliance review", "sourceRef": "nexora://projects/quill-controls", "summary": "Quill launch depends on contract taxonomy and regional retention validation."}),
    Record("Document", "doc-solstice-learning", {"title": "Solstice reliability plan", "sourceType": "Reliability plan", "sourceRef": "nexora://projects/solstice-learning", "summary": "Solstice begins with a compact signal set and standardized incident retrospectives."}),
    Record("Document", "doc-vela-thesis", {"title": "Vela ecosystem thesis", "sourceType": "Strategy memo", "sourceRef": "nexora://projects/vela-thesis", "summary": "Vela remains on hold until marketplace economics and extension controls are defined."}),
]

EXTRA_TEAMS = [
    Record("Team", "team-data", {"name": "Data Products", "description": "Data contracts, analytics foundations, and information quality."}),
    Record("Team", "team-customer-success", {"name": "Customer Success", "description": "Adoption, customer outcomes, and renewal readiness."}),
    Record("Team", "team-security", {"name": "Security Engineering", "description": "Threat detection, security architecture, and response."}),
    Record("Team", "team-design", {"name": "Experience Design", "description": "Research, service design, and accessible product experiences."}),
]

EXTRA_EMPLOYEES = [
    Record("Employee", "emp-yara", {"name": "Yara El-Sayed", "role": "Data Product Manager", "email": "yara@nexora.example", "location": "Cairo"}),
    Record("Employee", "emp-connor", {"name": "Connor Reed", "role": "Data Platform Engineer", "email": "connor@nexora.example", "location": "London"}),
    Record("Employee", "emp-rina", {"name": "Rina Kapoor", "role": "Customer Success Director", "email": "rina@nexora.example", "location": "Bengaluru"}),
    Record("Employee", "emp-ethan", {"name": "Ethan Brooks", "role": "Solutions Architect", "email": "ethan@nexora.example", "location": "Seattle"}),
    Record("Employee", "emp-leila", {"name": "Leila Haddad", "role": "Security Architect", "email": "leila@nexora.example", "location": "Paris"}),
    Record("Employee", "emp-jonas", {"name": "Jonas Fischer", "role": "Threat Detection Engineer", "email": "jonas@nexora.example", "location": "Berlin"}),
    Record("Employee", "emp-ana", {"name": "Ana Silva", "role": "Service Designer", "email": "ana@nexora.example", "location": "Lisbon"}),
    Record("Employee", "emp-omar", {"name": "Omar Khalil", "role": "UX Researcher", "email": "omar@nexora.example", "location": "Amman"}),
]

EXTRA_PROJECTS = [
    Record("Project", "proj-lighthouse", {"name": "Project Lighthouse", "status": "In Flight", "priority": "P1", "description": "Create a trusted data contract layer for cross-product reporting.", "dueDate": "2027-02-18"}),
    Record("Project", "proj-horizon", {"name": "Project Horizon", "status": "At Risk", "priority": "P0", "description": "Build a customer outcome program that connects adoption signals to renewal planning.", "dueDate": "2027-01-30"}),
    Record("Project", "proj-sentinel", {"name": "Project Sentinel", "status": "In Flight", "priority": "P0", "description": "Unify security telemetry, threat detection, and response playbooks.", "dueDate": "2027-02-26"}),
    Record("Project", "proj-mosaic", {"name": "Project Mosaic", "status": "Discovery", "priority": "P2", "description": "Design a consistent research and service blueprint for enterprise onboarding.", "dueDate": "2027-03-22"}),
]

EXTRA_TASKS = [
    ("task-lighthouse-contracts", "Define cross-product data contracts", "In Progress", "P1", "2027-01-05", "emp-yara", "proj-lighthouse"),
    ("task-lighthouse-quality", "Create data quality scorecards", "Open", "P1", "2027-01-14", "emp-connor", "proj-lighthouse"),
    ("task-lighthouse-lineage", "Map reporting lineage", "Blocked", "P1", "2027-01-21", "emp-connor", "proj-lighthouse"),
    ("task-lighthouse-pilot", "Pilot executive metrics", "Open", "P2", "2027-02-02", "emp-yara", "proj-lighthouse"),
    ("task-horizon-signals", "Define adoption health signals", "In Progress", "P0", "2026-12-20", "emp-rina", "proj-horizon"),
    ("task-horizon-playbook", "Draft renewal risk playbook", "Blocked", "P0", "2027-01-03", "emp-ethan", "proj-horizon"),
    ("task-horizon-accounts", "Select lighthouse accounts", "Done", "P1", "2026-12-05", "emp-rina", "proj-horizon"),
    ("task-horizon-review", "Run executive outcome review", "Open", "P1", "2027-01-18", "emp-ethan", "proj-horizon"),
    ("task-sentinel-schema", "Normalize security event schema", "In Progress", "P0", "2027-01-16", "emp-leila", "proj-sentinel"),
    ("task-sentinel-detection", "Tune priority detections", "In Progress", "P0", "2027-01-28", "emp-jonas", "proj-sentinel"),
    ("task-sentinel-response", "Exercise response playbooks", "Blocked", "P0", "2027-02-06", "emp-jonas", "proj-sentinel"),
    ("task-sentinel-audit", "Complete security audit pack", "Open", "P1", "2027-02-13", "emp-leila", "proj-sentinel"),
    ("task-mosaic-research", "Interview onboarding teams", "In Progress", "P2", "2027-02-12", "emp-omar", "proj-mosaic"),
    ("task-mosaic-blueprint", "Draft service blueprint", "Open", "P2", "2027-02-26", "emp-ana", "proj-mosaic"),
    ("task-mosaic-access", "Validate accessible flows", "Open", "P1", "2027-03-05", "emp-ana", "proj-mosaic"),
    ("task-mosaic-synthesis", "Synthesize enterprise themes", "Done", "P2", "2027-02-05", "emp-omar", "proj-mosaic"),
]

EXTRA_MEETINGS = [
    Record("Meeting", "meeting-116", {"title": "Data contract council", "date": "2026-11-04", "summary": "Set ownership for cross-product data contracts and agreed to publish quality scorecards."}),
    Record("Meeting", "meeting-117", {"title": "Customer outcomes review", "date": "2026-11-06", "summary": "Identified renewal risk caused by missing adoption signals and unclear account playbooks."}),
    Record("Meeting", "meeting-118", {"title": "Security telemetry summit", "date": "2026-11-08", "summary": "Prioritized normalized security events, detection tuning, and response exercises."}),
    Record("Meeting", "meeting-119", {"title": "Enterprise onboarding research", "date": "2026-11-10", "summary": "Aligned on interviews, service blueprint work, and accessibility validation."}),
]

EXTRA_DECISIONS = [
    Record("Decision", "decision-216", {"title": "Publish a shared data contract registry", "date": "2026-11-04", "status": "Active", "reason": "A visible registry will reduce conflicting definitions across executive and product reporting."}),
    Record("Decision", "decision-217", {"title": "Make adoption signals a renewal planning input", "date": "2026-11-06", "status": "At Risk", "reason": "Customer outcomes cannot be forecast reliably without consistent usage and adoption evidence."}),
    Record("Decision", "decision-218", {"title": "Prioritize detection quality over alert volume", "date": "2026-11-08", "status": "Active", "reason": "Security response capacity is limited, so high-confidence detections must come first."}),
    Record("Decision", "decision-219", {"title": "Use research before standardizing onboarding", "date": "2026-11-10", "status": "Active", "reason": "Enterprise onboarding needs evidence from multiple roles before a common blueprint is approved."}),
]

EXTRA_DOCUMENTS = [
    Record("Document", "doc-lighthouse-contracts", {"title": "Lighthouse data contract registry", "sourceType": "Data governance memo", "sourceRef": "nexora://projects/lighthouse-contracts", "summary": "Lighthouse establishes shared data contracts and quality scorecards for reporting."}),
    Record("Document", "doc-horizon-outcomes", {"title": "Horizon customer outcomes review", "sourceType": "Customer review", "sourceRef": "nexora://projects/horizon-outcomes", "summary": "Horizon connects adoption evidence to renewal risk and executive account reviews."}),
    Record("Document", "doc-sentinel-playbook", {"title": "Sentinel response playbook", "sourceType": "Security playbook", "sourceRef": "nexora://projects/sentinel-playbook", "summary": "Sentinel prioritizes normalized events, high-confidence detections, and exercised response paths."}),
    Record("Document", "doc-mosaic-research", {"title": "Mosaic onboarding research", "sourceType": "Research synthesis", "sourceRef": "nexora://projects/mosaic-research", "summary": "Mosaic uses enterprise interviews and accessibility validation before standardizing onboarding."}),
]


def _cypher_string(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _node_statement(record: Record) -> str:
    props = ", ".join(f"{key}: {_cypher_string(value)}" for key, value in {"id": record.id, **record.props}.items())
    return f"MERGE (n:{record.label} {{id: {_cypher_string(record.id)}}}) SET n += {{{props}}} RETURN n.id AS id"


def _relation_statement(source_label: str, source_id: str, relation: str, target_label: str, target_id: str) -> str:
    return (
        f"MATCH (a:{source_label} {{id: {_cypher_string(source_id)}}}), "
        f"(b:{target_label} {{id: {_cypher_string(target_id)}}}) "
        f"MERGE (a)-[:{relation}]->(b) RETURN count(*) AS linked"
    )


def seed_graph(db: FalkorDB) -> dict[str, int]:
    all_teams = TEAMS + MORE_TEAMS + DENSE_TEAMS + EXTRA_TEAMS
    all_employees = EMPLOYEES + MORE_EMPLOYEES + DENSE_EMPLOYEES + EXTRA_EMPLOYEES
    all_projects = PROJECTS + MORE_PROJECTS + DENSE_PROJECTS + EXTRA_PROJECTS
    all_meetings = MEETINGS + MORE_MEETINGS + DENSE_MEETINGS + EXTRA_MEETINGS
    all_decisions = DECISIONS + MORE_DECISIONS + DENSE_DECISIONS + EXTRA_DECISIONS
    all_documents = DOCUMENTS + MORE_DOCUMENTS + DENSE_DOCUMENTS + EXTRA_DOCUMENTS
    all_tasks = TASKS + MORE_TASKS + DENSE_TASKS + EXTRA_TASKS
    records = all_teams + all_employees + all_projects + all_meetings + all_decisions + all_documents + POLICIES
    records += [Record("Task", task_id, {"title": title, "status": status, "priority": priority, "dueDate": due, "description": f"{title} for the connected knowledge program."}) for task_id, title, status, priority, due, _, _ in all_tasks]
    upserted = 0
    for record in records:
        db.query(_node_statement(record))
        upserted += 1

    links: list[tuple[str, str, str, str, str]] = []
    team_for = {"emp-rahul": "team-product", "emp-priya": "team-product", "emp-lena": "team-product", "emp-maya": "team-engineering", "emp-owen": "team-engineering", "emp-daniel": "team-engineering", "emp-amara": "team-engineering", "emp-sofia": "team-growth", "emp-nikhil": "team-growth", "emp-jules": "team-growth", "emp-aisha": "team-research", "emp-victor": "team-platform", "emp-marcus": "team-operations", "emp-elena": "team-platform", "emp-tomas": "team-operations", "emp-grace": "team-operations", "emp-hiro": "team-ai", "emp-becca": "team-reliability", "emp-samir": "team-legal", "emp-nina": "team-partnerships", "emp-diego": "team-finance", "emp-mei": "team-product", "emp-arjun": "team-ai", "emp-fatima": "team-legal", "emp-chloe": "team-partnerships", "emp-ben": "team-growth", "emp-lucia": "team-finance", "emp-noah": "team-reliability", "emp-yara": "team-data", "emp-connor": "team-data", "emp-rina": "team-customer-success", "emp-ethan": "team-customer-success", "emp-leila": "team-security", "emp-jonas": "team-security", "emp-ana": "team-design", "emp-omar": "team-design"}
    for employee_id, team_id in team_for.items():
        links.append(("Employee", employee_id, "MEMBER_OF", "Team", team_id))
    links += [("Employee", "emp-rahul", "OWNS", "Project", "proj-phoenix"), ("Employee", "emp-maya", "OWNS", "Project", "proj-atlas"), ("Employee", "emp-amara", "OWNS", "Project", "proj-orion"), ("Employee", "emp-victor", "OWNS", "Project", "proj-nova"), ("Employee", "emp-marcus", "OWNS", "Project", "proj-helix"), ("Employee", "emp-aisha", "OWNS", "Project", "proj-cedar")]
    for task_id, _, _, _, _, owner_id, project_id in all_tasks:
        links += [("Employee", owner_id, "ASSIGNED_TO", "Task", task_id), ("Project", project_id, "HAS_TASK", "Task", task_id)]
    links += [("Meeting", "meeting-101", "RECORDED_DECISION", "Decision", "decision-201"), ("Meeting", "meeting-102", "RECORDED_DECISION", "Decision", "decision-202"), ("Meeting", "meeting-103", "RECORDED_DECISION", "Decision", "decision-203"), ("Meeting", "meeting-104", "RECORDED_DECISION", "Decision", "decision-204"), ("Meeting", "meeting-105", "RECORDED_DECISION", "Decision", "decision-205"), ("Meeting", "meeting-106", "RECORDED_DECISION", "Decision", "decision-206"), ("Meeting", "meeting-107", "RECORDED_DECISION", "Decision", "decision-207"), ("Meeting", "meeting-108", "RECORDED_DECISION", "Decision", "decision-208"), ("Meeting", "meeting-109", "RECORDED_DECISION", "Decision", "decision-209")]
    links += [("Decision", "decision-201", "DOCUMENTED_IN", "Document", "doc-phoenix"), ("Decision", "decision-202", "DOCUMENTED_IN", "Document", "doc-atlas-metrics"), ("Decision", "decision-203", "DOCUMENTED_IN", "Document", "doc-security"), ("Decision", "decision-206", "DOCUMENTED_IN", "Document", "doc-nova-charter"), ("Decision", "decision-207", "DOCUMENTED_IN", "Document", "doc-helix-playbook"), ("Decision", "decision-208", "DOCUMENTED_IN", "Document", "doc-cedar-research"), ("Decision", "decision-209", "DOCUMENTED_IN", "Document", "doc-helix-playbook"), ("Policy", "policy-leave", "DOCUMENTED_IN", "Document", "doc-leave"), ("Project", "proj-atlas", "DOCUMENTED_IN", "Document", "doc-atlas-metrics"), ("Project", "proj-orion", "DOCUMENTED_IN", "Document", "doc-orion-threat"), ("Project", "proj-nova", "DOCUMENTED_IN", "Document", "doc-nova-charter"), ("Project", "proj-helix", "DOCUMENTED_IN", "Document", "doc-helix-playbook"), ("Project", "proj-cedar", "DOCUMENTED_IN", "Document", "doc-cedar-research")]
    links += [("Team", "team-product", "SUPPORTS", "Project", "proj-phoenix"), ("Team", "team-engineering", "SUPPORTS", "Project", "proj-phoenix"), ("Team", "team-engineering", "SUPPORTS", "Project", "proj-atlas"), ("Team", "team-growth", "SUPPORTS", "Project", "proj-atlas"), ("Team", "team-engineering", "SUPPORTS", "Project", "proj-orion"), ("Team", "team-platform", "SUPPORTS", "Project", "proj-nova"), ("Team", "team-operations", "SUPPORTS", "Project", "proj-helix"), ("Team", "team-research", "SUPPORTS", "Project", "proj-cedar")]
    links += [("Project", "proj-phoenix", "HAS_DECISION", "Decision", "decision-201"), ("Project", "proj-phoenix", "HAS_DECISION", "Decision", "decision-205"), ("Project", "proj-atlas", "HAS_DECISION", "Decision", "decision-202"), ("Project", "proj-atlas", "HAS_DECISION", "Decision", "decision-204"), ("Project", "proj-orion", "HAS_DECISION", "Decision", "decision-203"), ("Project", "proj-nova", "HAS_DECISION", "Decision", "decision-206"), ("Project", "proj-helix", "HAS_DECISION", "Decision", "decision-207"), ("Project", "proj-helix", "HAS_DECISION", "Decision", "decision-209"), ("Project", "proj-cedar", "HAS_DECISION", "Decision", "decision-208"), ("Project", "proj-polaris", "HAS_DECISION", "Decision", "decision-210"), ("Project", "proj-meridian", "HAS_DECISION", "Decision", "decision-211"), ("Project", "proj-ember", "HAS_DECISION", "Decision", "decision-212"), ("Project", "proj-quill", "HAS_DECISION", "Decision", "decision-213"), ("Project", "proj-solstice", "HAS_DECISION", "Decision", "decision-214"), ("Project", "proj-vela", "HAS_DECISION", "Decision", "decision-215")]
    links += [("Task", "task-phoenix-assistant", "DEPENDS_ON", "Task", "task-phoenix-ingest"), ("Task", "task-atlas-dashboard", "DEPENDS_ON", "Task", "task-atlas-events"), ("Task", "task-orion-beta", "DEPENDS_ON", "Task", "task-orion-threat"), ("Task", "task-nova-health", "DEPENDS_ON", "Task", "task-nova-pipeline"), ("Task", "task-helix-training", "DEPENDS_ON", "Task", "task-helix-playbook"), ("Task", "task-cedar-synthesis", "DEPENDS_ON", "Task", "task-cedar-interviews"), ("Task", "task-polaris-datasets", "DEPENDS_ON", "Task", "task-polaris-eval"), ("Task", "task-polaris-risk", "DEPENDS_ON", "Task", "task-polaris-datasets"), ("Task", "task-meridian-retries", "DEPENDS_ON", "Task", "task-meridian-contract"), ("Task", "task-ember-approvals", "DEPENDS_ON", "Task", "task-ember-model"), ("Task", "task-quill-search", "DEPENDS_ON", "Task", "task-quill-taxonomy"), ("Task", "task-solstice-retro", "DEPENDS_ON", "Task", "task-solstice-signals"), ("Task", "task-vela-economics", "DEPENDS_ON", "Task", "task-vela-discovery")]
    links += [("Employee", "emp-hiro", "OWNS", "Project", "proj-polaris"), ("Employee", "emp-nina", "OWNS", "Project", "proj-meridian"), ("Employee", "emp-diego", "OWNS", "Project", "proj-ember"), ("Employee", "emp-samir", "OWNS", "Project", "proj-quill"), ("Employee", "emp-noah", "OWNS", "Project", "proj-solstice"), ("Employee", "emp-nina", "OWNS", "Project", "proj-vela")]
    links += [("Team", "team-ai", "SUPPORTS", "Project", "proj-polaris"), ("Team", "team-engineering", "SUPPORTS", "Project", "proj-polaris"), ("Team", "team-partnerships", "SUPPORTS", "Project", "proj-meridian"), ("Team", "team-reliability", "SUPPORTS", "Project", "proj-meridian"), ("Team", "team-finance", "SUPPORTS", "Project", "proj-ember"), ("Team", "team-product", "SUPPORTS", "Project", "proj-ember"), ("Team", "team-legal", "SUPPORTS", "Project", "proj-quill"), ("Team", "team-ai", "SUPPORTS", "Project", "proj-quill"), ("Team", "team-reliability", "SUPPORTS", "Project", "proj-solstice"), ("Team", "team-platform", "SUPPORTS", "Project", "proj-solstice"), ("Team", "team-partnerships", "SUPPORTS", "Project", "proj-vela"), ("Team", "team-finance", "SUPPORTS", "Project", "proj-vela")]
    links += [("Meeting", "meeting-110", "RECORDED_DECISION", "Decision", "decision-210"), ("Meeting", "meeting-111", "RECORDED_DECISION", "Decision", "decision-211"), ("Meeting", "meeting-112", "RECORDED_DECISION", "Decision", "decision-212"), ("Meeting", "meeting-113", "RECORDED_DECISION", "Decision", "decision-213"), ("Meeting", "meeting-114", "RECORDED_DECISION", "Decision", "decision-214"), ("Meeting", "meeting-115", "RECORDED_DECISION", "Decision", "decision-215")]
    links += [("Decision", "decision-210", "DOCUMENTED_IN", "Document", "doc-polaris-governance"), ("Decision", "decision-211", "DOCUMENTED_IN", "Document", "doc-meridian-readiness"), ("Decision", "decision-212", "DOCUMENTED_IN", "Document", "doc-ember-plan"), ("Decision", "decision-213", "DOCUMENTED_IN", "Document", "doc-quill-controls"), ("Decision", "decision-214", "DOCUMENTED_IN", "Document", "doc-solstice-learning"), ("Decision", "decision-215", "DOCUMENTED_IN", "Document", "doc-vela-thesis")]
    links += [("Project", "proj-polaris", "DOCUMENTED_IN", "Document", "doc-polaris-governance"), ("Project", "proj-meridian", "DOCUMENTED_IN", "Document", "doc-meridian-readiness"), ("Project", "proj-ember", "DOCUMENTED_IN", "Document", "doc-ember-plan"), ("Project", "proj-quill", "DOCUMENTED_IN", "Document", "doc-quill-controls"), ("Project", "proj-solstice", "DOCUMENTED_IN", "Document", "doc-solstice-learning"), ("Project", "proj-vela", "DOCUMENTED_IN", "Document", "doc-vela-thesis")]
    links += [("Project", "proj-polaris", "RELATED_TO", "Project", "proj-quill"), ("Project", "proj-quill", "RELATED_TO", "Project", "proj-orion"), ("Project", "proj-meridian", "RELATED_TO", "Project", "proj-atlas"), ("Project", "proj-ember", "RELATED_TO", "Project", "proj-vela"), ("Project", "proj-solstice", "RELATED_TO", "Project", "proj-nova"), ("Employee", "emp-hiro", "COLLABORATES_WITH", "Employee", "emp-arjun"), ("Employee", "emp-becca", "COLLABORATES_WITH", "Employee", "emp-noah"), ("Employee", "emp-samir", "COLLABORATES_WITH", "Employee", "emp-fatima"), ("Employee", "emp-nina", "COLLABORATES_WITH", "Employee", "emp-chloe"), ("Employee", "emp-diego", "COLLABORATES_WITH", "Employee", "emp-lucia")]
    links += [("Employee", "emp-yara", "OWNS", "Project", "proj-lighthouse"), ("Employee", "emp-rina", "OWNS", "Project", "proj-horizon"), ("Employee", "emp-leila", "OWNS", "Project", "proj-sentinel"), ("Employee", "emp-ana", "OWNS", "Project", "proj-mosaic")]
    links += [("Team", "team-data", "SUPPORTS", "Project", "proj-lighthouse"), ("Team", "team-engineering", "SUPPORTS", "Project", "proj-lighthouse"), ("Team", "team-customer-success", "SUPPORTS", "Project", "proj-horizon"), ("Team", "team-growth", "SUPPORTS", "Project", "proj-horizon"), ("Team", "team-security", "SUPPORTS", "Project", "proj-sentinel"), ("Team", "team-reliability", "SUPPORTS", "Project", "proj-sentinel"), ("Team", "team-design", "SUPPORTS", "Project", "proj-mosaic"), ("Team", "team-research", "SUPPORTS", "Project", "proj-mosaic")]
    links += [("Meeting", "meeting-116", "RECORDED_DECISION", "Decision", "decision-216"), ("Meeting", "meeting-117", "RECORDED_DECISION", "Decision", "decision-217"), ("Meeting", "meeting-118", "RECORDED_DECISION", "Decision", "decision-218"), ("Meeting", "meeting-119", "RECORDED_DECISION", "Decision", "decision-219")]
    links += [("Project", "proj-lighthouse", "HAS_DECISION", "Decision", "decision-216"), ("Project", "proj-horizon", "HAS_DECISION", "Decision", "decision-217"), ("Project", "proj-sentinel", "HAS_DECISION", "Decision", "decision-218"), ("Project", "proj-mosaic", "HAS_DECISION", "Decision", "decision-219")]
    links += [("Decision", "decision-216", "DOCUMENTED_IN", "Document", "doc-lighthouse-contracts"), ("Decision", "decision-217", "DOCUMENTED_IN", "Document", "doc-horizon-outcomes"), ("Decision", "decision-218", "DOCUMENTED_IN", "Document", "doc-sentinel-playbook"), ("Decision", "decision-219", "DOCUMENTED_IN", "Document", "doc-mosaic-research")]
    links += [("Project", "proj-lighthouse", "DOCUMENTED_IN", "Document", "doc-lighthouse-contracts"), ("Project", "proj-horizon", "DOCUMENTED_IN", "Document", "doc-horizon-outcomes"), ("Project", "proj-sentinel", "DOCUMENTED_IN", "Document", "doc-sentinel-playbook"), ("Project", "proj-mosaic", "DOCUMENTED_IN", "Document", "doc-mosaic-research")]
    links += [("Project", "proj-lighthouse", "RELATED_TO", "Project", "proj-polaris"), ("Project", "proj-horizon", "RELATED_TO", "Project", "proj-meridian"), ("Project", "proj-sentinel", "RELATED_TO", "Project", "proj-orion"), ("Project", "proj-mosaic", "RELATED_TO", "Project", "proj-cedar"), ("Employee", "emp-yara", "COLLABORATES_WITH", "Employee", "emp-connor"), ("Employee", "emp-rina", "COLLABORATES_WITH", "Employee", "emp-ethan"), ("Employee", "emp-leila", "COLLABORATES_WITH", "Employee", "emp-jonas"), ("Employee", "emp-ana", "COLLABORATES_WITH", "Employee", "emp-omar")]
    linked = 0
    for source_label, source_id, relation, target_label, target_id in links:
        db.query(_relation_statement(source_label, source_id, relation, target_label, target_id))
        linked += 1
    return {"nodesUpserted": len(records), "relationshipsUpserted": linked}
