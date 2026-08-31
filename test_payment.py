import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent


async def main():
    runner = InMemoryRunner(agent=root_agent)

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="demo-user",
        session_id="payment-demo",
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="""An incident has been reported for payment-api.

Act as Joro, an autonomous Google Cloud operations agent.

Investigate the incident using the available service health and logs.
Correlate the evidence and determine whether this is a transient failure
or a configuration/root-cause issue.

If the evidence indicates that a restart is safe and justified, use the
restart_service tool.

After taking the corrective action, ALWAYS use verify_service_recovery
to verify whether the service recovered.

Clearly report:
1. What you observed.
2. Your root-cause assessment.
3. Whether a restart is appropriate.
4. Whether you took the restart action.
5. The verification result."""
            )
        ],
    )

    async for event in runner.run_async(
        user_id="demo-user",
        session_id="payment-demo",
        new_message=user_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())
