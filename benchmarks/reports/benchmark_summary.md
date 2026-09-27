# Applied AI Agent Archetypes: Cross-Archetype Benchmark Report

**Execution Mode:** `MOCK` | **Model:** `gemini-2.5-flash` | **Timestamp:** `2026-09-27 18:42:20 UTC`

---

## 1. Executive Summary & Comparative Matrix

| # | Agent Archetype | Williams' Classification | Mean Latency | P95 Latency | Tokens (Prompt / Comp) | Cost / 1k Runs | Conformance |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| 1 | **Stock & News Monitor** | Autonomous Monitoring Loop | 53.09 ms | 56.05 ms | 249 (185/64) | $0.0331 | 100.0% |
| 2 | **Deep Researcher** | Goal Decomposition & Plan-Execute | 134.77 ms | 145.03 ms | 1230 (850/380) | $0.1778 | 98.5% |
| 3 | **Support Triage Router** | Autonomy Spectrum & Policy Escalation | 71.97 ms | 76.73 ms | 450 (340/110) | $0.0585 | 100.0% |
| 4 | **Travel Agency Debate** | Collaborative Multi-Agent Debate | 200.06 ms | 215.05 ms | 1980 (1420/560) | $0.2745 | 99.0% |

---

## 2. Architectural Systems Trade-offs & Failure Modes

### Project 1: Stock & News Monitor (Autonomous Monitoring Loop)
- **Williams' Properties:** `Moderate Autonomy` · `Low Social Ability (Isolated Agent)`
- **Latency SLA:** Mean: `53.09 ms` · P95: `56.05 ms`
- **Token Economics:** `249 total tokens` (`185` prompt / `64` completion) → `$0.0331 per 1,000 invocations`
- **Key Systems Bottleneck:** Polling frequency vs rate-limiting overhead
- **Architectural Mitigation:** SQLite episodic hash deduplication stops redundant LLM queries

### Project 2: Deep Researcher (Goal Decomposition & Plan-Execute)
- **Williams' Properties:** `High Proactivity / Bounded Autonomy` · `Low Social Ability (Sequential Sub-tasks)`
- **Latency SLA:** Mean: `134.77 ms` · P95: `145.03 ms`
- **Token Economics:** `1230 total tokens` (`850` prompt / `380` completion) → `$0.1778 per 1,000 invocations`
- **Key Systems Bottleneck:** Sequential multi-hop query synthesis compounding latency
- **Architectural Mitigation:** Subtask fan-out with citation verification contracts

### Project 3: Support Triage Router (Autonomy Spectrum & Policy Escalation)
- **Williams' Properties:** `Gated Autonomy (HITL Fallback)` · `Moderate Social Ability (Human Handoff)`
- **Latency SLA:** Mean: `71.97 ms` · P95: `76.73 ms`
- **Token Economics:** `450 total tokens` (`340` prompt / `110` completion) → `$0.0585 per 1,000 invocations`
- **Key Systems Bottleneck:** Vector similarity variance & false-positive autonomous execution
- **Architectural Mitigation:** Strict confidence threshold gating (0.85) routing ambiguous cases to Tier 2

### Project 4: Travel Agency Debate (Collaborative Multi-Agent Debate)
- **Williams' Properties:** `High Social Ability / Bounded Autonomy` · `High Social Ability (Planner <-> Accountant)`
- **Latency SLA:** Mean: `200.06 ms` · P95: `215.05 ms`
- **Token Economics:** `1980 total tokens` (`1420` prompt / `560` completion) → `$0.2745 per 1,000 invocations`
- **Key Systems Bottleneck:** Multi-turn context window inflation during adversarial rounds
- **Architectural Mitigation:** ConversationBuffer with max round caps (MAX_ROUNDS=4) & structured proposals

---

## 3. Fleet Aggregate Performance

- **Fleet Average Latency:** `114.97 ms`
- **Total Suite Token Footprint:** `3909 tokens`
- **Aggregate Cost for 1,000 Suite Iterations:** `$0.5439`
- **Contract & Schema Conformance:** `99.38%`

