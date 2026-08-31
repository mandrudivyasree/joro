# JORO — Autonomous Google Cloud Operations Agent

JORO is an autonomous cloud operations agent that investigates service incidents, analyzes available health information, logs, and metrics, decides whether a corrective action is appropriate, and verifies the result after taking action.

The main idea behind JORO is simple: an unhealthy service should not automatically be restarted. The agent should first understand what is happening and then decide what action, if any, is justified.

## How It Works

JORO follows this operational workflow:

```text
OBSERVE
   |
   v
INVESTIGATE
   |
   v
CORRELATE
   |
   v
DECIDE
   |
   +---- No action required
   |
   v
ACT
   |
   v
VERIFY
```

The agent uses multiple tools during an investigation and bases its decision on the evidence returned by those tools.

## Example Scenarios

### checkout-api

In this scenario, JORO detects an unhealthy service with:

* 37% error rate
* 92% CPU utilization
* 4.8 second request latency
* HTTP 503 errors
* Container startup failures
* A missing `DATABASE_URL` environment variable

JORO identifies the missing environment variable as a persistent configuration problem.

It decides not to restart the service because restarting would not resolve the underlying configuration issue.

Result:

```text
Incident detected
       |
       v
Investigate health, logs and metrics
       |
       v
Configuration problem identified
       |
       v
Restart not justified
       |
       v
No restart performed
```

### payment-api

In this scenario, JORO detects:

* 18% error rate
* HTTP 503 errors
* Temporary health-check failures
* A transient container failure
* No configuration errors

The evidence indicates a temporary failure, so JORO determines that restarting the service is a safe and reasonable corrective action.

It then calls the restart tool and verifies the service afterward.

Result:

```text
Incident detected
       |
       v
Investigate health and logs
       |
       v
Transient failure identified
       |
       v
Restart justified
       |
       v
Restart performed
       |
       v
Recovery verified
```

## Agent Tools

JORO currently has access to the following operational tools:

| Tool                          | Purpose                                                  |
| ----------------------------- | -------------------------------------------------------- |
| `get_service_health`          | Checks service health and error information              |
| `get_recent_logs`             | Retrieves recent service logs                            |
| `get_simulated_metric_status` | Provides performance metrics for incident scenarios      |
| `get_cpu_utilization`         | Reads CPU utilization from Google Cloud Monitoring       |
| `check_for_incidents`         | Determines whether CPU utilization indicates an incident |
| `restart_service`             | Performs a controlled simulated service restart          |
| `verify_service_recovery`     | Verifies whether the service recovered                   |
| `get_payment_service_health`  | Provides health information for the payment scenario     |
| `get_payment_service_logs`    | Provides logs for the payment scenario                   |

## Safety Rules

JORO is designed to operate within explicit boundaries.

The agent is instructed to:

* Observe before acting.
* Investigate before making a decision.
* Correlate multiple sources of evidence.
* Prefer the least disruptive corrective action.
* Never delete resources.
* Never modify IAM permissions.
* Never change billing or project configuration.
* Never expose secrets or credentials.
* Never restart a service without evidence that a restart is appropriate.
* Verify recovery after taking a corrective action.

The agent can therefore decide that taking no action is the correct outcome.

## Technology

JORO is built with:

* Python
* Google ADK
* Gemini
* Google Cloud
* Google Cloud Monitoring
* FastAPI

Google ADK is used to build the agent and connect it with the operational tools. Gemini provides the reasoning layer used to investigate incidents and determine the appropriate course of action.

Google Cloud Monitoring is used for the CPU utilization check.

FastAPI provides the API layer used to interact with JORO from the demonstration interface.

## Project Structure

```text
joro/
├── agent.py
├── cloud_tools.py
├── server.py
├── test_joro.py
├── test_payment.py
├── tools/
│   └── cloud_tools.py
└── web/
    └── index.html
```

## Running the Project

### 1. Start the API server

From the project directory:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

The API will be available locally on port 8000.

### 2. Investigate checkout-api

Send an incident to JORO:

```bash
curl -X POST http://127.0.0.1:8000/investigate \
-H "Content-Type: application/json" \
-d '{"service":"checkout-api"}'
```

JORO should investigate the service and identify the missing configuration as the root cause. It should decide that restarting the service is not appropriate.

### 3. Investigate payment-api

```bash
curl -X POST http://127.0.0.1:8000/investigate \
-H "Content-Type: application/json" \
-d '{"service":"payment-api"}'
```

For this scenario, JORO should identify the failure as transient, perform the controlled restart, and verify recovery.

## Running the Agent Directly

The agent can also be tested without the API layer.

For the checkout scenario:

```bash
python test_joro.py
```

For the payment scenario:

```bash
python test_payment.py
```

These tests demonstrate the agent's investigation and decision-making process directly through Google ADK.

## API Response

The investigation endpoint returns a structured response containing the service name and JORO's incident report.

A typical response includes:

```text
Observations
Root Cause Assessment
Restart Decision
Action Taken
Verification Result
```

This makes the reasoning and resulting operational action visible instead of hiding the decision inside the agent.

## Why JORO

Traditional monitoring systems are good at detecting that something is wrong, but detection alone does not resolve an incident.

JORO focuses on the next steps:

```text
Detect
  ↓
Investigate
  ↓
Understand
  ↓
Decide
  ↓
Act when justified
  ↓
Verify
```

The important behavior is not simply that JORO can restart a service. It is that JORO can distinguish between situations where restarting makes sense and situations where it does not.

## Current Scope

This project is a controlled prototype demonstrating autonomous incident investigation and remediation.

The restart operation used in the demonstration is intentionally controlled and simulated. The project does not make unrestricted production infrastructure changes.

The architecture can be extended to connect additional Google Cloud services and real operational actions.

## Future Improvements

Possible extensions include:

* Integration with Cloud Logging for richer log analysis
* Additional Cloud Run and Compute Engine diagnostics
* More incident types and remediation actions
* Dependency-aware incident correlation
* Budget and quota monitoring
* Persistent incident history
* Human approval for higher-impact actions
* Integration with Cloud Monitoring alerting
* Production-grade authentication and authorization

## Project Goal

JORO explores how an AI agent can move beyond simply reporting cloud incidents and instead participate in the operational loop:

**Investigate the problem, make a reasoned decision, take a safe action when appropriate, and verify the outcome.**

