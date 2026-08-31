import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent


async def main():
    runner = InMemoryRunner(agent=root_agent)
    await runner.session_service.create_session(
    app_name=runner.app_name,
    user_id="demo-user",
    session_id="demo-session",
  )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="An incident has been reported for checkout-api. Act as Joro, an autonomous Google Cloud operations agent. Investigate the incident using the service health, recent logs, and available metrics. Correlate the evidence and identify the root cause. Decide whether a restart is appropriate. If a restart is safe and justified, use the restart_service tool. If it is not appropriate, do not restart. Clearly report your investigation, decision, and action."
            )
        ],
    )

    async for event in runner.run_async(
        user_id="demo-user",
        session_id="demo-session",
        new_message=user_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())
