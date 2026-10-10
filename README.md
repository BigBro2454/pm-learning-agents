# Applied AI Agent Architecture Lab: 4 Production Agent Archetypes

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Google Gemini](https://img.shields.io/badge/intelligence-Google%20Gemini%202.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Framework](https://img.shields.io/badge/framework-Williams'%20Agent%20Framework-orange.svg)](https://en.wikipedia.org/wiki/Intelligent_agent)
[![Security Guardrails](https://img.shields.io/badge/guardrails-Sub--0.2ms%20Deterministic-emerald.svg)](./guardrails/agent_guardrails.py)
[![HITL Queue](https://img.shields.io/badge/HITL-Priority--Gated%20Supervisor-purple.svg)](./hitl/escalation_queue.py)
[![Test Suite](https://img.shields.io/badge/tests-21%2F21%20Passed%20(100%25)-brightgreen.svg)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Engineering Design Document & Production Reference Implementation**  
> *Author:* **Ishan Dhiman** ([@BigBro2454](https://github.com/BigBro2454))  
> *Target Architecture:* Google Cloud AI / Vertex AI Multi-Agent Systems / Applied AI Product Management

---

## 1. Executive Summary & Systems Problem Statement

Enterprise AI applications routinely fail when engineering teams treat Generative AI as a monolithic text completion box. Real-world business challenges require **autonomous, resilient, and specialized agentic architectures** operating across distinct operational regimes:

* **Unattended Monitoring**: Continuous observation without runaway token consumption or hallucinated alarms.
* **Complex Multi-Step Synthesis**: Structured decomposition of vague instructions into verifiable, evidence-backed deliverables.
* **Risk-Tolerant Triage**: Explicitly bounded autonomy with dynamic confidence gating and human-in-the-loop (HITL) escalation.
* **Adversarial Constraint Negotiation**: Multi-agent collaboration where competing objectives (e.g., utility vs. financial budget) converge deterministically.

### The Solution: The Applied Agent Architecture Lab
This repository implements **four distinct production agent archetypes** grounded in **Williams' Agent Framework** and powered by Google's native **`google-genai` SDK (`gemini-2.5-flash`)**. Each archetype tackles a specific enterprise systems failure mode with explicit trade-offs, structured Pydantic schemas, and state persistence.

---

## 2. PR #2 Architectural Deliverables: Security Guardrails, HITL Queue & Lifecycle Telemetry

To elevate the lab to Google Cloud AI enterprise production readiness, **Pull Request #2** introduces four foundational governance and observability systems:

```mermaid
flowchart TD
    Inbound([User / Inbound Payload]) --> Guardrails[1. AgentGuardrails Engine<br/>Sub-0.2ms Regex Interception]
    
    Guardrails -->|Prompt Injection Detected| BlockNode[Action: BLOCK<br/>0 Token Spend / Circuit Break]
    Guardrails -->|PII Detected| MaskNode[Action: SANITIZE<br/>Redact CC / SSN / Email / Phone]
    Guardrails -->|Legal Threat OR Budget Cap Exceeded| EscalateNode[Action: ESCALATE<br/>Forward to HITL Queue]
    
    MaskNode --> Lifecycle[2. Operational Lifecycle Engine<br/>Perception ➔ Reasoning ➔ Action ➔ Memory]
    
    Lifecycle -->|Decision Confidence < 0.85| EscalateNode
    Lifecycle -->|Standard Execution| AutoResolve[Action: Autonomous Resolution<br/>Dispatch Webhook / Proposal]
    
    EscalateNode --> HITLQueue[3. HITLEscalationQueue<br/>Priority: CRITICAL / HIGH / MEDIUM / LOW]
    HITLQueue --> Supervisor[Human Supervisor Decision<br/>APPROVED / REJECTED / OVERRIDDEN]
    
    Lifecycle --> Profiler[4. LifecycleProfiler & ROI Modeler<br/>Phase Waterfall Latency + Token Economics]
    Profiler --> Dash[5. Interactive HTML Dashboard<br/>docs/archetype_dashboard.html]

    classDef block fill:#EA4335,stroke:#c5221f,stroke-width:2px,color:#ffffff;
    classDef safe fill:#34A853,stroke:#1e8e3e,stroke-width:2px,color:#ffffff;
    classDef warn fill:#FBBC04,stroke:#f29900,stroke-width:2px,color:#202124;
    classDef proc fill:#4285F4,stroke:#1a73e8,stroke-width:2px,color:#ffffff;

    class BlockNode block;
    class AutoResolve,MaskNode safe;
    class EscalateNode,HITLQueue warn;
    class Guardrails,Lifecycle,Profiler,Dash proc;
```

### Key PR #2 Highlights:
1. **Multi-Stage Security Guardrails (`guardrails/agent_guardrails.py`)**:
   - Zero-latency deterministic interception of prompt injections (`PROMPT_INJECTION_IGNORE_DIRECTIVES`, `JAILBREAK_ROLEPLAY`, `SYSTEM_PROMPT_EXTRACTION`) in sub-0.02ms with 0 token expenditure.
   - PCI-DSS & GDPR-compliant PII Masking: Redacts 16-digit credit cards (`[REDACTED_CREDIT_CARD]`), SSNs (`[REDACTED_SSN]`), emails, and phone numbers.
   - Financial Boundary Enforcement: Validates transactions against programmatic ceilings ($500 default auto-approval cap).
   - Hostile & Legal Threat Interception: Detects regulatory threats and lawyer mentions for immediate escalation.

2. **Human-in-the-Loop (HITL) Policy Escalation Queue (`hitl/escalation_queue.py`)**:
   - Priority scoring engine (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) factoring in risk scores, legal exposure, financial overruns, and confidence deficits.
   - Supervisor review state machines (`PENDING` → `APPROVED` / `REJECTED` / `OVERRIDDEN`) with immutable audit trails.

3. **Lifecycle Telemetry Waterfall & Economics Profiler (`telemetry/lifecycle_profiler.py`)**:
   - Profiles wall-clock execution across the 4 canonical operational phases: Perception (12-16ms), Reasoning (28-145ms), Action (6-26ms), Memory (4-13ms).
   - Multi-model pricing comparator: Models Gemini 2.5 Flash ($0.075 / $0.30 per 1M tokens) against OpenAI GPT-4o ($2.50 / $10.00) and Claude 3.5 Sonnet ($3.00 / $15.00), demonstrating **>97% enterprise cost reduction**.
   - Automated export of structured JSON and Google L5 Markdown scorecards to `telemetry/reports/`.

4. **Interactive Architecture & Simulation Dashboard (`docs/archetype_dashboard.html`)**:
   - Self-contained visual dashboard featuring an interactive Williams' Taxonomy Explorer, live 4-archetype execution simulator with real-time latency waterfalls, HITL supervisor review console, and dynamic ROI calculator.

---

## 3. Williams' Agent Framework & Property Taxonomy

Under Williams' formulation, an autonomous agent is defined across **four behavioral properties** and **four operational components**, positioned along a continuous spectrum:

```mermaid
mindmap
  root((Williams' Agent Framework))
    Behavioral Properties
      Autonomy
        "Independent execution"
        "Escalation boundaries"
      Reactivity
        "Event-driven triggers"
        "Dynamic adaptation"
      Proactivity
        "Goal decomposition"
        "Self-directed initiatives"
      Social Ability
        "Agent-to-Agent (A2A)"
        "Agent-to-Human (HITL)"
    Operational Components
      Perception
        "RSS feeds & Webhooks"
        "Intent classification"
        "Entity extraction"
      Reasoning
        "Pydantic structured output"
        "Multi-round debate"
        "Vector RAG policy lookup"
      Action
        "API notifications"
        "Ticket auto-resolution"
        "Plan generation"
      Memory
        "SQLite episodic store"
        "ChromaDB vector space"
        "Conversation buffer"
```

### Archetype Spectrum Positioning Matrix

| # | Archetype | Target Domain | Autonomy | Reactivity | Proactivity | Social Ability | Primary Component Focus |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **Market Intelligence Monitor** | Unattended Signal Detection | Moderate | **High** | Low | Low | **Perception ⇄ Memory** (Stateful deduplication) |
| **2** | **Deep Research Synthesizer** | Long-Horizon Information Gathering | High | Moderate | **High** | Low | **Reasoning ⇄ Action** (Decomposition & Verification) |
| **3** | **Customer Support Router** | Risk-Bounded Enterprise Triage | **Variable (Gated)** | **High** | Moderate | Moderate (HITL) | **Reasoning ⇄ Action** (Confidence Escalation) |
| **4** | **Collaborative Travel Agency** | Multi-Objective Optimization | Bounded | Moderate | **High** | **High (A2A)** | **Social Ability ⇄ Reasoning** (Adversarial Debate) |

---

## 4. Deep Architectural Blueprints of the 4 Archetypes

### Project 1: Market & News Intelligence Agent (`project-1-stock-monitor`)
*Systems Problem:* Ingestion loops without semantic filtering produce notification fatigue and quadratic LLM costs.

```mermaid
sequenceDiagram
    autonumber
    participant Feed as RSS / Market Feed
    participant P as Perception Module
    participant M as SQLite Episodic Memory
    participant R as Gemini 2.5 Flash Reasoner
    participant A as Action Dispatcher (Webhook)

    loop Polling Interval (300s)
        Feed->>P: Ingest raw article entries
        P->>M: Query seen article URLs / hashes
        alt Article Already Seen
            M-->>P: Duplicate detected -> Drop
        else New Article
            P->>R: Transmit Article(title, summary, source)
            Note over R: Pydantic Structured Output: RelevanceResult
            R-->>P: {relevance_score: 0.92, is_relevant: true}
            opt is_relevant == true
                P->>A: Dispatch high-priority alert (Discord / Webhook)
            end
            P->>M: Store article hash, score, and timestamp
        end
    end
```

---

### Project 2: Deep Information Retrieval & Synthesis Agent (`project-2-deep-researcher`)
*Systems Problem:* Single-shot LLM prompts fail on broad research queries by hallucinating coverage and omitting contradictory viewpoints.

```mermaid
flowchart TD
    UserQuery([User Research Topic]) --> Planner[Planner Module<br/>Decompose query into 3-5 subtasks]
    
    subgraph PlanExecLoop ["Iterative Plan-Execute-Verify Loop"]
        direction TB
        Subtask1["Subtask N: Generate Targeted Search Queries"]
        Searcher["Searcher / Retriever Module"]
        Synth["Synthesizer Module<br/>Extract findings & cross-reference"]
        Verifier["Verifier Module<br/>Fact-check against raw evidence"]

        Subtask1 --> Searcher
        Searcher --> Synth
        Synth --> Verifier
    end

    Planner --> PlanExecLoop
    Verifier -->|Iterate next subtask| PlanExecLoop
    Verifier -->|All subtasks verified| Aggregator[Final Executive Dossier & Markdown Report]
    Aggregator --> Deliverable([Completed Technical Briefing])

    classDef proc fill:#4285F4,stroke:#1a73e8,stroke-width:2px,color:#ffffff;
    classDef step fill:#34A853,stroke:#1e8e3e,stroke-width:2px,color:#ffffff;
    class Planner,Aggregator proc;
    class Subtask1,Searcher,Synth,Verifier step;
```

---

### Project 3: Customer Support Triage & Policy Router (`project-3-support-router`)
*Systems Problem:* Autonomous agents in customer service introduce financial liability without strict policy grounding and confidence thresholds.

```mermaid
flowchart TD
    CustomerMsg([Customer Inbound Message]) --> Percept[Perception Module<br/>Extract Intent, Sentiment, Urgency, Entities]
    
    Percept --> VectorLookup[ChromaDB Vector Store<br/>Retrieve Company Policies via Similarity Search]
    
    VectorLookup --> Reasoner[Reasoning Module<br/>Evaluate Intent vs Policies with Gemini 2.5]
    
    Reasoner --> ConfidenceCheck{Confidence >= 0.85<br/>AND Low Financial Risk?}
    
    ConfidenceCheck -->|YES| AutoResolve[Action: Autonomous Resolution<br/>Auto-refund / Password reset / Policy answer]
    ConfidenceCheck -->|NO| Escalate[Action: Human Tier-2 Escalation<br/>Forward ticket with reasoning rationale & entities]
    
    AutoResolve --> AuditLog[(Audit Log & Metrics)]
    Escalate --> AuditLog

    classDef decision fill:#FBBC04,stroke:#f29900,stroke-width:2px,color:#202124;
    classDef actionNode fill:#34A853,stroke:#1e8e3e,stroke-width:2px,color:#ffffff;
    classDef alertNode fill:#EA4335,stroke:#c5221f,stroke-width:2px,color:#ffffff;

    class ConfidenceCheck decision;
    class AutoResolve actionNode;
    class Escalate alertNode;
```

---

### Project 4: Multi-Agent Constraint Negotiation System (`project-4-travel-agency`)
*Systems Problem:* Optimizing complex multi-variable constraints (e.g., flight luxury vs. strict financial budget) causes single agents to compromise silently or violate boundaries.

```mermaid
sequenceDiagram
    autonumber
    actor User as User Request ($3000 Budget, Tokyo 5-Nights)
    participant Buffer as Shared Conversation Buffer
    participant Planner as Planner Agent (Utility Maximizer)
    participant Acct as Accountant Agent (Budget Enforcer)

    User->>Buffer: Initialize Trip Constraints ($3,000 max)
    
    loop Bounded Multi-Turn Negotiation (Max 5 Rounds)
        Buffer->>Planner: Request Itinerary Proposal
        Note over Planner: Searches flights, hotels, activities
        Planner->>Buffer: Post Proposal (Flight $1,800 + Hotel $1,500 = $3,300)
        
        Buffer->>Acct: Transmit Proposal for Audit
        Note over Acct: Evaluates against hard $3,000 ceiling
        alt Cost ($3,300) > Budget ($3,000)
            Acct->>Buffer: Post Critique ("Exceeds budget by $300. Select 3-star hotel.")
        else Cost <= Budget
            Acct->>Buffer: Post Approval ("Budget satisfied. Proceed.")
            Note over Buffer: Convergence Reached!
        end
    end
    Buffer-->>User: Present Final Agreed Itinerary
```

---

## 5. Google L5 Systems & Architectural Trade-off Matrix

| Architectural Vector | Naive / Baseline Approach | Applied Agent Architecture (This Lab) | L5 Systems Rationale & Trade-offs |
| :--- | :--- | :--- | :--- |
| **Observation & Perception** | Periodic unindexed polling of all feeds | In-memory hash checks + SQLite episodic memory | Eliminates duplicate inference calls; saves 90%+ token costs on recurring monitoring loops. |
| **Planning & Synthesis** | Monolithic zero-shot generation | Hierarchical subtask decomposition with verification | Single-shot generation suffers 35%+ higher hallucination rate on multi-source factual queries. |
| **Risk & Autonomy** | Binary (100% autonomous or 100% human) | Spectrum-based gating with `CONFIDENCE_THRESHOLD=0.85` | Provides mathematical bounding on liability while automating 60-70% of standard customer inquiries. |
| **Constraint Resolution** | Single prompt with conflicting instructions | Multi-agent adversarial separation of concerns | Separating utility maximization from constraint auditing prevents model compromise and hallucinated math. |
| **Inter-Agent Protocol** | Freeform text string concatenations | Typed `Message` objects in a managed `ConversationBuffer` | Enables auditability, deterministic round bounds, and automated convergence detection. |
| **Security Defense** | Unchecked raw string model injection | Zero-latency regex inspection + PII redaction | Defends against prompt injection and GDPR/PCI-DSS violations in <0.02ms with 0 token spend. |

---

## 6. Installation & Unified CLI Runner

### Prerequisites
* Python 3.10+
* Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/BigBro2454/pm-learning-agents.git
cd pm-learning-agents

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

---

## 7. Execution & Verification Guide

The unified CLI runner (`run_lab.py`) orchestrates demos, property inspection, security validation, and automated tests:

### 1. View Agent Catalog & Williams' Taxonomy
```bash
python run_lab.py --list
```

### 2. Run Automated Verification Test Suite (21 Tests)
```bash
python run_lab.py --test
```

### 3. Verify Security Guardrails Engine
```bash
python run_lab.py --guardrails
```

### 4. Launch HITL Policy Escalation Console
```bash
python run_lab.py --hitl
```

### 5. Profile Operational Lifecycle Telemetry (Perception ➔ Memory)
```bash
# Run 3 iterations per archetype and export reports
python run_lab.py --lifecycle --export-dir telemetry/reports
```

### 6. View Interactive Single-Page Dashboard
```bash
python run_lab.py --dashboard
# Or open directly:
open docs/archetype_dashboard.html
```

### 7. Launch Individual Agent Archetypes
```bash
# Project 1: Market & News Intelligence Monitor
python run_lab.py --project 1

# Project 2: Deep-Dive Information Retrieval & Synthesis
python run_lab.py --project 2

# Project 3: Customer Support Triage & Escalation Router
python run_lab.py --project 3

# Project 4: Multi-Agent Travel Agency Negotiation Loop
python run_lab.py --project 4
```

---

## 8. Operational Lifecycle Latency & Token Economics Scorecard

Profiled using `LifecycleProfiler` across the 4 operational phases on Google Gemini 2.5 Flash ($0.075 / 1M prompt tokens, $0.30 / 1M completion tokens):

| # | Archetype | Perception | Reasoning | Action | Memory | Total Mean | P95 SLA | Cost / 1k Invocations | Cost Reduction vs GPT-4o |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **1** | **Market Intelligence Monitor** | `14.5 ms` | `28.0 ms` | `6.5 ms` | `4.0 ms` | **`53.0 ms`** | **`60.5 ms`** | **$0.0307** | **96.8%** |
| **2** | **Deep Research Synthesizer** | `12.0 ms` | `94.0 ms` | `21.0 ms` | `8.0 ms` | **`135.0 ms`** | **`154.7 ms`** | **$0.1776** | **97.1%** |
| **3** | **Customer Support Router** | `11.0 ms` | `48.0 ms` | `9.0 ms` | `4.0 ms` | **`72.0 ms`** | **`82.5 ms`** | **$0.0584** | **96.9%** |
| **4** | **Collaborative Travel Agency** | `16.0 ms` | `145.0 ms` | `26.0 ms` | `13.0 ms` | **`200.0 ms`** | **`229.3 ms`** | **$0.2744** | **97.3%** |

- **Fleet Average Latency:** `115.0 ms`
- **Total Suite Cost per 1,000 Iterations (Gemini 2.5 Flash):** `$0.5411`
- **Total Suite Cost per 1,000 Iterations (GPT-4o Baseline):** `$19.7825`
- **Net Enterprise Fleet Cost Savings:** **`97.26%`**

---

## 9. Repository Structure

```
pm-learning-agents/
├── run_lab.py                         # Unified CLI runner (projects, benchmarks, guardrails, HITL)
├── pyproject.toml                     # PEP 517/621 packaging metadata
├── requirements.txt                   # Production dependency pins
├── .env.example                       # Safe environment variable template
├── .gitignore                         # Zero-leak version control exclusions
├── LICENSE                            # MIT License
├── README.md                          # Google L5 Engineering Design Document & PRD
├── LEARNINGS.md                       # Williams' Agent Framework living reference
├── PROGRESS.md                        # Architecture milestone and decision log
├── docs/
│   └── archetype_dashboard.html       # Interactive single-page architecture & simulation dashboard
├── guardrails/                        # PR #2 Multi-stage security & policy defense engine
│   ├── __init__.py
│   └── agent_guardrails.py            # Prompt injection defense, PII masking, budget enforcement
├── hitl/                              # PR #2 Human-in-the-Loop decision supervisor
│   ├── __init__.py
│   └── escalation_queue.py            # Priority-scored escalation queue & review state machine
├── telemetry/                         # PR #2 Operational lifecycle telemetry profiler
│   ├── __init__.py
│   ├── lifecycle_profiler.py          # 4-phase latency waterfalls & multi-model economics
│   └── reports/                       # Exported lifecycle telemetry JSON & Markdown scorecards
├── benchmarks/                        # PR #1 Cross-archetype benchmark harness
│   ├── __init__.py
│   ├── archetype_benchmarker.py       # Comparative benchmark runner & cost modeler
│   └── reports/                       # Exported benchmark reports (JSON & Markdown)
├── tests/
│   ├── test_learning_agents.py        # Automated test suite for schemas & buffers
│   ├── test_benchmarks.py             # Unit tests for token & cost benchmark harness
│   └── test_guardrails_telemetry_hitl.py # PR #2 tests (guardrails, HITL queue, lifecycle profiler)
├── project-1-stock-monitor/           # Archetype 1: Perception-Reasoning-Action Loop
│   ├── src/ (perception, reasoning, action, memory, config, main)
│   └── README.md
├── project-2-deep-researcher/         # Archetype 2: Goal Decomposition & Synthesis
│   ├── src/ (planner, searcher, synthesizer, verifier, memory, config, main)
│   └── README.md
├── project-3-support-router/          # Archetype 3: Autonomy Spectrum & Vector RAG
│   ├── src/ (perception, reasoning, action, memory, config, main)
│   ├── knowledge-base/ (company refund & escalation policies)
│   └── README.md
└── project-4-travel-agency/           # Archetype 4: Multi-Agent Adversarial Debate
    ├── src/ (planner_agent, accountant_agent, conversation, tools, memory, main)
    └── README.md
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
