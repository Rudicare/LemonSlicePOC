import os
import asyncio
from dotenv import load_dotenv
from vision_agents.core import Agent, User
from vision_agents.plugins import getstream, openai

load_dotenv()

async def send_test():
    client = Agent(
        edge=getstream.Edge(
            api_key=os.getenv("STREAM_API_KEY"),
            api_secret=os.getenv("STREAM_API_SECRET"),
            provide_audio=False,
            provide_video=False,
            session_id="rudi-poc-test" # MUST MATCH BOT
        ),
        agent_user=User(name="Tester", id="test-user"),
        llm=openai.Realtime(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    )

    try:
        print("🔗 Joining Rudi's room...")
        await asyncio.sleep(2) # Give it a second to join
        
        print("✉️ Sending: 'Hello Rudi!'")
        await client.say("Hello Rudi! Are you there?")
        
        print("⏳ Waiting 5 seconds for Rudi to process...")
        await asyncio.sleep(5) # CRITICAL: Keep connection open to receive response
        
    finally:
        await client.close()
        print("✅ Test finished.")

if __name__ == "__main__":
    asyncio.run(send_test())