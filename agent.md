# Agent Context — PM Learning: Autonomous Agents

> **Purpose:** This file provides context to any AI agent (Gemini, Claude, etc.) working in this repository. Read this first before touching any project.

## 🧭 What Is This Repository?

This is a **hands-on learning lab** built around Williams' framework for autonomous agents from the PM Learning curriculum (Book 4). It contains **four progressive projects**, each designed to isolate and deeply explore specific properties, components, and lifecycle phases of production-grade autonomous agents.

The learner is **Ishan**, who is studying product management with a focus on AI-native products. The goal is not just theoretical understanding—it's to build working prototypes that reveal the real-world nuances and failure modes of agentic systems.

---

## 📁 Repository Structure

```
pm-learning-agents/
├── agent.md                          ← YOU ARE HERE (AI context file)
├── PROGRESS.md                       ← Decision log, milestones, status tracker
├── LEARNINGS.md                      ← Conceptual notes, flowcharts, revision material
│
├── project-1-stock-monitor/          ← Reactivity & Perception
│   ├── README.md                     ← Project spec, architecture, setup
│   └── src/                          ← Source code
│
├── project-2-deep-researcher/        ← Proactivity & Agent Lifecycle
│   ├── README.md
│   └── src/
│
├── project-3-support-router/         ← Autonomy Spectrum & Memory
│   ├── README.md
│   ├── knowledge-base/              ← Mock KB docs for vector store
│   └── src/
│
└── project-4-travel-agency/          ← Social Ability & Multi-Agent
    ├── README.md
    └── src/
```

---

## 🧠 Core Framework (Williams)

### Four Agent Properties (exist on a spectrum)
| Property | Definition | Key Nuance |
|---|---|---|
| **Autonomy** | Operates without constant human oversight | Production agents escalate edge cases |
| **Reactivity** | Perceives and responds to environmental changes | Must filter noise, avoid infinite loops |
| **Proactivity** | Takes initiative toward goal achievement | Requires robust planning & decomposition |
| **Social Ability** | Communicates with other agents or humans | Enables multi-agent collaboration |

### Four Core Components
| Component | Function | Failure Mode to Watch |
|---|---|---|
| **Perception** | Ingests inputs from the environment | Noisy data, missed events, format errors |
| **Reasoning** | Analyzes information, plans actions | Hallucination, poor decomposition, loops |
| **Action** | Executes decisions via external systems | API failures, wrong tool selection, side effects |
| **Memory** | Stores/retrieves past experiences & context | Stale data, retrieval misses, context overflow |

### Agent Loop
`Perceive → Reason → Act → Observe → Store → Repeat`

### Agent Lifecycle (5 Phases)
`Task Reception → Planning → Execution → Verification → Delivery`

---

## 📐 Project Mapping to Concepts

| Project | Primary Focus | Secondary Focus |
|---|---|---|
| **1 — Stock Monitor** | Perception, Reactivity | Memory (episodic log), basic Action |
| **2 — Deep Researcher** | Proactivity, Agent Lifecycle | Reasoning (planning), Verification |
| **3 — Support Router** | Autonomy Spectrum | Memory (vector store), escalation logic |
| **4 — Travel Agency** | Social Ability | Multi-agent reasoning, conversation memory |

---

## 🛠️ Tech Stack (Planned)
- **Language:** Python 3.11+
- **LLM SDK:** Google Gemini API (`google-genai`)
- **Vector Store:** ChromaDB (local, lightweight)
- **Database:** SQLite (episodic logs, state)
- **Notifications:** Discord webhooks / email (SMTP)
- **Web Search:** Tavily API or SerpAPI (for Project 2)

---

## 📝 Conventions for AI Agents Working Here

1. **Always read `PROGRESS.md`** before making changes to understand current status.
2. **Always update `PROGRESS.md`** after completing work — log what was done, decisions made, and next steps.
3. **Add conceptual insights to `LEARNINGS.md`** whenever a new nuance or failure mode is discovered.
4. **Each project's `README.md`** is the source of truth for that project's architecture, setup, and status.
5. **Never delete or overwrite learning notes** — append to them.
6. **Code goes in `src/`** within each project folder.
7. **Use clear, well-commented code** — this is a learning repo, readability > cleverness.

---

## 🔄 Current Status

| Project | Status | Last Updated |
|---|---|---|
| 1 — Stock Monitor | 🟡 Initialized | 2026-08-21 |
| 2 — Deep Researcher | 🟡 Initialized | 2026-08-21 |
| 3 — Support Router | 🟡 Initialized | 2026-08-21 |
| 4 — Travel Agency | 🟡 Initialized | 2026-08-21 |
