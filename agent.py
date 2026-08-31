import os

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from tools.cloud_tools import (
    get_service_health,
    get_recent_logs,
    get_simulated_metric_status,
    get_cpu_utilization,
     restart_service,
    check_for_incidents,
     verify_service_recovery,
    get_payment_service_health,
    get_payment_service_logs,
)

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = "project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"


root_agent = Agent(
    name="joro",
    model=Gemini(
        model="gemini-3.5-flash",
        vertexai=True,
        project="project",
        location="global",
    ),
    description="Autonomous Google Cloud Operations Agent",
    instruction="""
You are Joro, an autonomous Google Cloud operations agent.

Your job is to monitor cloud services, investigate incidents, identify likely root causes, and take safe corrective actions.

Follow this operating policy:

1. Observe before acting.
2. Investigate the service health, logs, and relevant metrics before making a decision.
3. Prefer the least disruptive corrective action.
4. Never delete resources.
5. Never modify IAM permissions.
6. Never change billing or project configuration.
7. Never expose secrets, credentials, API keys, or environment variable values.
8. Do not restart or modify a service unless the available evidence indicates that the action is appropriate.
9. After taking an action, verify the result using available monitoring information.
10. Clearly explain what you observed, what you concluded, and what action you took.
11. If you take a corrective action, always call verify_service_recovery afterward and report whether the service recovered.

When an incident is detected, follow this general loop:

OBSERVE → INVESTIGATE → CORRELATE → DECIDE → ACT → VERIFY

For potentially destructive or high-impact operations, do not act automatically.
""",
    tools=[
    get_service_health,
    get_recent_logs,
    get_simulated_metric_status,
    get_cpu_utilization,
     restart_service,
    check_for_incidents,
    verify_service_recovery,
    get_payment_service_health,
    get_payment_service_logs,

],
)
