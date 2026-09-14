# 📊 Progress & Decision Log

> Track all milestones, architectural decisions, blockers, and status changes here.
> AI agents: **always update this file** after completing work.

---

## Status Dashboard

| # | Project | Status | Started | Last Activity | Blockers |
|---|---------|--------|---------|---------------|----------|
| 1 | Stock/News Monitor | ✅ Complete | 2026-08-21 | 2026-08-21 | None |
| 2 | Deep-Dive Researcher | ✅ Complete | 2026-08-21 | 2026-08-21 | None |
| 3 | Customer Support Router | ✅ Complete | 2026-08-21 | 2026-08-21 | None |
| 4 | Travel Agency (Multi-Agent) | ✅ Complete | 2026-08-21 | 2026-08-21 | None |

**Status Legend:** 🔴 Blocked | 🟡 Not Started / Initialized | 🟢 In Progress | ✅ Complete | ⏸️ Paused

---

## Decision Log

### DEC-001: Project Ordering & Progression
- **Date:** 2026-08-21
- **Decision:** Build projects in sequence (1 → 2 → 3 → 4) because each builds on concepts from the previous.
- **Rationale:** Project 1 teaches the fundamental Agent Loop. Project 2 adds planning complexity. Project 3 introduces the autonomy spectrum. Project 4 combines everything into multi-agent communication.
- **Alternatives Considered:** Building all in parallel — rejected because later projects assume familiarity with earlier concepts.

### DEC-002: Tech Stack Selection
- **Date:** 2026-08-21
- **Decision:** Python + Gemini API + ChromaDB + SQLite
- **Rationale:**
  - Python: Most mature ecosystem for LLM tooling.
  - Gemini API: Accessible, well-documented, generous free tier.
  - ChromaDB: Zero-config vector store, perfect for local prototyping (Project 3).
  - SQLite: Embedded DB, no server needed, great for episodic logs.
- **Alternatives Considered:**
  - LangChain/LangGraph — rejected for now to understand primitives first, may revisit.
  - OpenAI API — viable alternative, Gemini chosen for Google ecosystem familiarity.

### DEC-003: Learning-First Code Philosophy
- **Date:** 2026-08-21
- **Decision:** Prioritize readable, well-commented code over production optimization.
- **Rationale:** This is a learning repo. Every function should teach a concept. Comments should explain *why*, not just *what*.

---

## Changelog

### 2026-08-21 — Repository Initialization
- Created repository structure with 4 project folders.
- Wrote `agent.md` (AI context), `PROGRESS.md` (this file), `LEARNINGS.md` (concepts & flowcharts).
- Initialized each project with a detailed `README.md` containing:
  - Concept mapping to Williams' framework
  - Architecture overview
  - Component breakdown
  - Implementation plan
  - Success criteria
- **Next Steps:** Begin building Project 1 — Stock/News Monitor.

### 2026-08-21 — Project 1 (Stock Monitor) Implemented
- Implemented the full agent loop (Perception, Reasoning, Action, Memory).
- Created `perception.py` using `feedparser` for RSS feed ingestion.
- Created `reasoning.py` using `google-genai` and structured outputs for relevance scoring.
- Created `memory.py` using `sqlite3` to prevent duplicate alerts.
- Created `action.py` for mock/discord webhook notifications.

### 2026-08-21 — Project 2 (Deep Researcher) Implemented
- Implemented the 5-phase agent lifecycle.
- Created `planner.py` for goal decomposition and subtask generation.
- Created `searcher.py` with mock/Tavily responses for finding data.
- Created `synthesizer.py` and `verifier.py` to evaluate research completeness.
- Uses `sqlite3` in `memory.py` to store complete lifecycle logs.

### 2026-08-21 — Project 3 (Support Router) Implemented
- Implemented the Autonomy Spectrum using Confidence Thresholds.
- Set up `ChromaDB` for Semantic Memory with a markdown knowledge base.
- Created `perception.py` for intent and sentiment classification.
- Created `reasoning.py` for matching intents with policies.
- Configured dynamic escalation vs. autonomous resolution based on risk and confidence.

### 2026-08-21 — Project 4 (Travel Agency) Implemented
- Implemented a multi-agent negotiation system.
- Created `planner_agent.py` (optimistic travel planner) and `accountant_agent.py` (strict budget reviewer).
- Configured tools in `tools.py` for mock flight/hotel lookups and cost calculation.
- Created `conversation.py` buffer to allow back-and-forth negotiation.
- Created an orchestrator loop in `main.py` that handles deadlock detection and convergence.

---

## Backlog & Ideas
- [ ] Add unit tests per project to validate agent behavior
- [ ] Create a shared `utils/` module if common patterns emerge across projects
- [ ] Consider adding a `benchmarks/` folder to measure agent performance (latency, accuracy)
- [ ] Explore adding LangSmith or similar observability for tracing agent loops
- [ ] After all 4 projects, write a "meta-learnings" synthesis document
