# 🧠 Learnings & Concept Reference

> A living document for revision. Contains conceptual notes, flowcharts, and insights discovered while building. **Never delete — only append.**

---

## Table of Contents
- [1. Williams' Agent Framework](#1-williams-agent-framework)
- [2. The Agent Loop](#2-the-agent-loop)
- [3. The Agent Lifecycle](#3-the-agent-lifecycle)
- [4. Agent Properties Spectrum](#4-agent-properties-spectrum)
- [5. Core Components Deep-Dive](#5-core-components-deep-dive)
- [6. Failure Modes & Anti-Patterns](#6-failure-modes--anti-patterns)
- [7. Project-Specific Insights](#7-project-specific-insights)

---

## 1. Williams' Agent Framework

Williams defines an autonomous agent through **four properties** and **four components**. The key insight is that these exist on a **spectrum** — no agent is fully autonomous or fully reactive. Production agents are tuned along these axes based on the risk and complexity of the domain.

```mermaid
mindmap
  root((Autonomous Agent))
    Properties
      Autonomy
        "Operates independently"
        "Escalates edge cases"
      Reactivity
        "Responds to environment"
        "Event-driven behavior"
      Proactivity
        "Takes initiative"
        "Goal decomposition"
      Social Ability
        "Agent-to-agent comms"
        "Agent-to-human comms"
    Components
      Perception
        "API webhooks"
        "Document parsers"
        "Sensor feeds"
      Reasoning
        "LLM inference"
        "Planning algorithms"
        "Prompt templates"
      Action
        "Tool calls"
        "API invocations"
        "Code execution"
      Memory
        "Vector stores"
        "Conversation buffers"
        "Episodic logs"
```

---

## 2. The Agent Loop

The fundamental execution pattern of every agent, regardless of complexity:

```mermaid
graph LR
    A["🔍 Perceive"] --> B["🧠 Reason"]
    B --> C["⚡ Act"]
    C --> D["👁️ Observe Result"]
    D --> E["💾 Store in Memory"]
    E --> A

    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#FF9800,color:#fff
    style D fill:#9C27B0,color:#fff
    style E fill:#607D8B,color:#fff
```

### Key Insight
> Williams emphasizes that **production failures almost always trace back to a breakdown in one of the four components** rather than model capability. The model is rarely the bottleneck — it's the plumbing around it.

### Where Things Break (by component)

| Loop Phase | Component | Common Failure |
|---|---|---|
| Perceive | Perception | Missing events, wrong format, noisy data |
| Reason | Reasoning | Hallucinated plans, infinite loops, wrong tool selection |
| Act | Action | API timeout, wrong parameters, unintended side effects |
| Observe & Store | Memory | Stale context, retrieval misses, buffer overflow |

---

## 3. The Agent Lifecycle

Williams describes a 5-phase lifecycle for production agents. This is the *macro* view (the Agent Loop is the *micro* view that happens inside the Execution phase).

```mermaid
graph TD
    T["📥 1. Task Reception"] --> P["📋 2. Planning"]
    P --> E["⚙️ 3. Execution"]
    E --> V{"✅ 4. Verification"}
    V -->|"Pass"| D["📤 5. Delivery"]
    V -->|"Fail: re-plan"| P
    E -->|"Tool failure: retry"| E

    T -.->|"API call / user request / scheduled trigger"| T
    D -.->|"Log outcomes & update episodic memory"| D

    style T fill:#26A69A,color:#fff
    style P fill:#42A5F5,color:#fff
    style E fill:#FFA726,color:#fff
    style V fill:#AB47BC,color:#fff
    style D fill:#66BB6A,color:#fff
```

### Phase Details

| Phase | What Happens | Critical Question |
|---|---|---|
| **Task Reception** | Agent receives a goal (API, trigger, user) | Is the goal well-defined enough to act on? |
| **Planning** | Decompose goal → subtasks, select tools | Can the agent recover if the plan is wrong? |
| **Execution** | Iteratively call tools, process results, update plan | What happens when a tool call fails? |
| **Verification** | Evaluate output against goal criteria | How does the agent know it succeeded? |
| **Delivery** | Return results, log outcomes, update memory | Is the episodic memory useful for future tasks? |

---

## 4. Agent Properties Spectrum

Agents are not binary. Each property is a dial, not a switch.

```mermaid
quadrantChart
    title Agent Properties Positioning
    x-axis "Low Reactivity" --> "High Reactivity"
    y-axis "Low Autonomy" --> "High Autonomy"
    quadrant-1 "Fully Autonomous Agent"
    quadrant-2 "Proactive Monitor"
    quadrant-3 "Manual Tool"
    quadrant-4 "Reactive Bot"
    "Project 1 - Stock Monitor": [0.8, 0.3]
    "Project 2 - Researcher": [0.4, 0.6]
    "Project 3 - Support Router": [0.5, 0.7]
    "Project 4 - Travel Agency": [0.6, 0.85]
```

### The Autonomy Spectrum in Practice

```mermaid
graph LR
    A["Fully Manual"] --> B["Copilot / Suggest"]
    B --> C["Act with Approval"]
    C --> D["Act & Report"]
    D --> E["Fully Autonomous"]

    style A fill:#EF5350,color:#fff
    style B fill:#FF7043,color:#fff
    style C fill:#FFA726,color:#fff
    style D fill:#66BB6A,color:#fff
    style E fill:#26A69A,color:#fff
```

**Project 3** specifically explores this spectrum: the agent handles routine queries autonomously but escalates complex/risky cases to a human.

---

## 5. Core Components Deep-Dive

### Perception
- **What it does:** Transforms raw environmental data into structured information the Reasoning component can use.
- **Production implementations:** API webhooks, RSS feeds, database triggers, file watchers, user messages.
- **Key insight:** Perception is a *filter*. A good perception layer reduces noise so the Reasoning component isn't overwhelmed.

### Reasoning
- **What it does:** The "brain" — analyzes perceived information, creates plans, selects tools, makes decisions.
- **Production implementations:** LLM inference chains, prompt templates, rule engines, planning algorithms.
- **Key insight:** Reasoning is where most *visible* failures happen (hallucinations, bad plans), but the *root cause* is often bad Perception or Memory feeding it garbage data.

### Action
- **What it does:** The "hands" — executes decisions by calling tools and APIs.
- **Production implementations:** Function calling, API invocations, database writes, code execution.
- **Key insight:** Actions have **side effects**. Unlike Perception and Reasoning (which are read-only), a bad Action can cause real damage. This is why Verification exists.

### Memory
- **What it does:** Stores and retrieves context, past experiences, and knowledge.
- **Types:**
  - **Short-term / Working memory:** Current conversation buffer, in-context window.
  - **Episodic memory:** Logs of past agent runs and outcomes (SQLite, logs).
  - **Semantic memory:** Long-term knowledge retrieval (vector stores, knowledge graphs).
- **Key insight:** Memory is the most underestimated component. Without good memory, agents repeat mistakes, lose context, and can't learn from experience.

```mermaid
graph TD
    subgraph "Memory Types"
        ST["🧠 Short-Term<br/>Conversation buffer<br/>Context window"]
        EP["📓 Episodic<br/>Past runs & outcomes<br/>SQLite / logs"]
        SM["📚 Semantic<br/>Knowledge retrieval<br/>Vector stores"]
    end

    ST -->|"Current task context"| R["Reasoning"]
    EP -->|"What worked before?"| R
    SM -->|"Domain knowledge"| R

    style ST fill:#42A5F5,color:#fff
    style EP fill:#66BB6A,color:#fff
    style SM fill:#AB47BC,color:#fff
    style R fill:#FFA726,color:#fff
```

---

## 6. Failure Modes & Anti-Patterns

> Add entries here as you discover them while building.

| # | Failure Mode | Component | Description | Discovered In |
|---|---|---|---|---|
| F-001 | Infinite Alert Loop | Perception + Memory | Agent keeps alerting on the same event because memory doesn't track "already seen" | — |
| F-002 | Hallucinated Tool Call | Reasoning | Agent invents a tool name that doesn't exist | — |
| F-003 | Plan Decomposition Failure | Reasoning | Agent creates a plan with steps it cannot actually execute | — |
| F-004 | Stale Context | Memory | Agent uses outdated information from an old conversation | — |
| F-005 | Overconfident Autonomy | Action | Agent takes a high-risk action without verification or escalation | — |

---

## 7. Project-Specific Insights

> Append learnings here as each project progresses.

### Project 1 — Stock/News Monitor
_No insights yet. Will be populated during development._

### Project 2 — Deep-Dive Researcher
_No insights yet._

### Project 3 — Customer Support Router
_No insights yet._

### Project 4 — Travel Agency
_No insights yet._
