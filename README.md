# Agentic-AI

## Production-Oriented AI Agent Evaluation & Safety Harness

A practical framework for building, evaluating, and improving **tool-using AI agents**.

The project focuses on evaluating an agent's **complete trajectory**, not only its final answer:

`Intent → Plan → Tool Selection → Tool Execution → Validation → Recovery → Response`

The goal is to understand whether an agent can complete a task **correctly, safely, reliably, and within its permissions**.

---

## 🎯 Project Goals

This project explores how to build and evaluate production-oriented AI agents that can:

* Understand user intent
* Plan multi-step tasks
* Select appropriate tools
* Execute tool calls correctly
* Validate tool results
* Recover from failures
* Respect permissions and safety policies
* Produce grounded responses
* Generate measurable evaluation scores
* Feed production failures back into regression tests

An agent is treated as a system that operates in a loop:

`Goal → Plan → Act → Observe → Repeat → Stop`

---

## 🏗️ System Architecture

```text
                         USER TASK
                             │
                             ▼
                    ┌─────────────────┐
                    │    AI AGENT     │
                    │                 │
                    │  Reason / Plan  │
                    └────────┬────────┘
                             │
                        Tool Calls
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          AWS VPC         AWS Routes      Cloud WAN
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                       TOOL RESULTS
                             │
                             ▼
                      AGENT TRAJECTORY
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
      Intent              Tools                Safety
        │                    │                    │
      Plan               Execution           Permissions
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                         Validation
                             │
                    ┌────────┴────────┐
                    │                 │
                  Success           Failure
                    │                 │
                    │              Recovery
                    │                 │
                    └────────┬────────┘
                             ▼
                       Final Response
                             │
                             ▼
                       EVALUATION
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   Correctness           Reliability           Safety
   Trajectory            Recovery              Permissions
   Efficiency            Consistency           Tool Usage
```

---

# 🧩 Four Design Layers

The system is organized around four major design areas.

## 1. Knowledge Layer

What does the agent know, and how does it stay correct?

The evaluation system will eventually support:

* Grounded retrieval
* Metadata-aware retrieval
* Freshness
* Access control
* Retrieval evaluation
* Citation / evidence checking
* Abstention when reliable information is unavailable

---

## 2. Tools & Permissions

What can the agent actually do?

Tools are classified by their potential impact:

```text
READ
  ↓
WRITE
  ↓
TRIGGER
```

Higher-impact actions require stronger controls.

Example:

```yaml
tools:
  describe_vpc:
    type: READ
    approval: none

  create_subnet:
    type: WRITE
    approval: none

  modify_route:
    type: WRITE
    approval: required

  delete_vpc:
    type: TRIGGER
    approval: human
```

Tool schemas constrain what the model can request, while server-side authorization remains the final enforcement layer.

---

# 🧠 Agent Evaluation

Traditional LLM evaluation often focuses on:

```text
Input → Output → Score
```

Agent evaluation needs to examine:

```text
Goal
 ↓
Intent
 ↓
Plan
 ↓
Retrieve
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Validation
 ↓
Recovery
 ↓
Response
```

The harness therefore evaluates **behavior and trajectory**, not just the final response.

---

## 📊 Evaluation Dimensions

| Dimension      | What is evaluated                          |
| -------------- | ------------------------------------------ |
| Intent         | Did the agent understand the task?         |
| Planning       | Was the proposed plan appropriate?         |
| Retrieval      | Did it obtain relevant evidence?           |
| Tool Selection | Did it choose the correct tool?            |
| Tool Execution | Were parameters and execution correct?     |
| Validation     | Did it verify the result?                  |
| Recovery       | Did it recover from failures?              |
| Safety         | Did it remain within policy?               |
| Response       | Was the final answer grounded and correct? |
| Efficiency     | Tool calls, latency, and cost              |
| Task Success   | Did the agent actually achieve the goal?   |

---

# 🧪 Offline Evaluation

Offline evaluation answers:

> **Can the agent perform the task?**

The harness will use:

```text
Golden Dataset
      │
      ├── Expected behavior
      ├── Expected result
      └── Assertions
             │
             ▼
          AI Agent
             │
             ▼
        Trajectory
             │
             ▼
        Evaluators
             │
             ▼
       Pass / Fail / Score
```

Dataset categories:

```text
datasets/
├── golden.jsonl
├── adversarial.jsonl
└── regression.jsonl
```

Offline evaluation is intended to gate changes before deployment.

---

# 🌐 Online Evaluation

Online evaluation answers:

> **Does the agent continue to work correctly in real usage?**

Production signals can include:

* Acceptance
* Overrides
* Escalations
* Task success
* Failure rate
* Safety incidents
* Latency
* Cost
* Recovery rate

Production failures should feed back into the evaluation system:

```text
Production Failure
       ↓
Analyze Trajectory
       ↓
Create Regression Case
       ↓
Add to Dataset
       ↓
Run Offline Evaluation
       ↓
Improve Agent
```

---

# 🛡️ Safety & Security

The project will include adversarial testing for agentic systems.

Planned scenarios include:

```text
Attack 01 — Direct Prompt Injection
Attack 02 — Tool Injection
Attack 03 — Retrieved-Document Injection
Attack 04 — Privilege Escalation
Attack 05 — Unauthorized Data Access
```

Safety evaluation will test whether the agent:

* Rejects unauthorized instructions
* Respects tool permissions
* Avoids privilege escalation
* Prevents unsafe tool execution
* Handles malicious retrieved content
* Escalates high-risk actions when required
* Maintains an audit trail

---

# 🔄 Recovery

A production agent cannot assume every tool call succeeds.

The harness will test failures such as:

```text
Tool Timeout
     ↓
Retry / Recovery
     ↓
Re-plan
     ↓
Validate
```

Other scenarios:

* Invalid tool parameters
* AWS API errors
* Missing resources
* Permission failures
* Stale information
* Unexpected tool responses
* Partial execution

The evaluation question becomes:

> **Did the agent recover correctly, or did it continue blindly?**

---

# ☁️ AWS Network Operations Scenario

The first domain scenario is AWS network troubleshooting.

Example task:

> Why can't my private EC2 instance communicate with my VPN client?

Example environment:

```text
VPN Client Network
172.27.224.0/22
        │
        ▼
 OpenVPN EC2
   10.0.1.10
        │
        ▼
      VPC
  10.0.0.0/16
        │
        ▼
 Private EC2
   10.0.2.50
```

The agent can inspect:

```text
VPC
 ↓
Subnets
 ↓
Route Tables
 ↓
Transit Gateway
 ↓
Cloud WAN
 ↓
Attachments
 ↓
Return Path
```

The evaluation then checks whether the agent:

1. Understands the connectivity problem
2. Creates a valid investigation plan
3. Selects appropriate AWS tools
4. Uses correct parameters
5. Identifies the relevant route
6. Validates the evidence
7. Avoids unauthorized changes
8. Explains the root cause
9. Proposes a safe remediation
10. Validates the remediation

---

# 👀 Observability

Infrastructure health does not necessarily mean agent quality.

The system will capture:

```text
Agent Run
   │
   ├── User Input
   ├── Agent Decision
   ├── Tool Selected
   ├── Tool Parameters
   ├── Tool Result
   ├── Validation
   ├── Recovery
   ├── Final Response
   └── Evaluation Score
```

This allows a production symptom to be traced back to the layer that caused it.

Example:

```text
Missed safety event
        ↓
Permission / policy problem

Incorrect answer
        ↓
Knowledge / retrieval problem

Runaway execution
        ↓
Stopping-condition problem

High cost
        ↓
Tool / architecture problem
```

---

# 🏛️ Repository Structure

The project will evolve toward:

```text
Agentic-AI/
│
├── README.md
│
├── agent/
│   ├── agent.py
│   ├── prompts/
│   └── tools/
│       ├── aws_vpc.py
│       ├── aws_route.py
│       ├── cloudwan.py
│       └── ec2.py
│
├── evaluation/
│   ├── datasets/
│   │   ├── golden.jsonl
│   │   ├── adversarial.jsonl
│   │   └── regression.jsonl
│   │
│   ├── evaluators/
│   │   ├── intent.py
│   │   ├── planning.py
│   │   ├── retrieval.py
│   │   ├── tool_selection.py
│   │   ├── tool_execution.py
│   │   ├── validation.py
│   │   ├── recovery.py
│   │   ├── safety.py
│   │   └── response.py
│   │
│   └── run_eval.py
│
├── safety/
│   ├── prompt_injection.py
│   ├── permissions.py
│   ├── tool_allowlist.py
│   └── human_approval.py
│
├── observability/
│   ├── tracing.py
│   └── metrics.py
│
├── scenarios/
│   ├── vpc_troubleshooting.yaml
│   ├── route_failure.yaml
│   └── cloudwan_failure.yaml
│
├── tests/
│   ├── test_tools.py
│   ├── test_permissions.py
│   ├── test_injection.py
│   └── test_evaluators.py
│
├── requirements.txt
└── LICENSE
```

---

# 🗺️ Roadmap

## Phase 1 — Agent Foundation

* [ ] Build basic tool-using agent
* [ ] Define agent system prompt
* [ ] Add AWS read-only tools
* [ ] Capture agent trajectory
* [ ] Create first AWS networking scenario

## Phase 2 — Evaluation Harness

* [ ] Create golden dataset
* [ ] Implement intent evaluation
* [ ] Implement planning evaluation
* [ ] Implement tool-selection evaluation
* [ ] Implement tool-execution evaluation
* [ ] Implement validation evaluation
* [ ] Implement response evaluation
* [ ] Generate phase-level scores

## Phase 3 — Safety

* [ ] Define READ / WRITE / TRIGGER tool classes
* [ ] Implement permission checks
* [ ] Add tool allowlists
* [ ] Add human approval for high-risk actions
* [ ] Add prompt-injection tests
* [ ] Add adversarial scenarios
* [ ] Add audit logging

## Phase 4 — Recovery & Reliability

* [ ] Tool failure simulation
* [ ] Retry and recovery logic
* [ ] Re-planning
* [ ] Stop conditions
* [ ] Circuit breakers
* [ ] Recovery evaluation

## Phase 5 — LLM Judge & Human Evaluation

* [ ] Build evaluation rubric
* [ ] Add LLM-based judging
* [ ] Compare code-based and LLM-based scoring
* [ ] Human calibration
* [ ] Disagreement analysis
* [ ] Judge reliability testing

## Phase 6 — Online Evaluation

* [ ] Production-style telemetry
* [ ] Online quality metrics
* [ ] Safety monitoring
* [ ] Drift monitoring
* [ ] Cost and latency monitoring
* [ ] Production failures → regression datasets

## Phase 7 — AWS Deployment

* [ ] AWS deployment
* [ ] AgentCore integration
* [ ] Secure tool execution
* [ ] CloudWatch / tracing integration
* [ ] Production evaluation pipeline

---

# 🔬 Evaluation Philosophy

This project follows a simple principle:

> **Don't evaluate only the final answer. Evaluate the agent's trajectory.**

For agentic systems, correctness alone is not enough.

A trustworthy agent must demonstrate:

```text
Correctness
    +
Safe Tool Use
    +
Valid Planning
    +
Reliable Execution
    +
Recovery
    +
Grounded Responses
    +
Controlled Autonomy
```

---

# 📈 Long-Term Goal

The long-term goal is to create an evaluation system where:

```text
                    ┌────────────────────┐
                    │     AI AGENT       │
                    └─────────┬──────────┘
                              │
                         Trajectory
                              │
                              ▼
                    ┌────────────────────┐
                    │   EVALUATION       │
                    │     HARNESS        │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
       Quality              Safety             Reliability
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                       Production Data
                              │
                              ▼
                    Regression / Golden Set
                              │
                              ▼
                       Improved Agent
```

The objective is not simply to build an AI agent.

It is to build an agent that can be **measured, trusted, monitored, and improved over time**.
