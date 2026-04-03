import os
import asyncio
from dotenv import load_dotenv

# Core imports from vision-agents
from vision_agents.core import Agent, User
from vision_agents.core.processors import Processor
from vision_agents.plugins import getstream, openai

# Load environment variables
load_dotenv()

class LemonSliceProcessor(Processor):
    @property
    def name(self) -> str:
        return "lemonslice_sync"

    async def close(self):
        pass

    async def __call__(self, event):
        # 🔥 This is what we are looking for in the terminal!
        if event.type == "agent.response.text.done":
            print(f"\n🎬 [LemonSlice] SUCCESS! Rudi is speaking: {event.text[:60]}...")
            # Phase 1 Integration:
            # avatar_id = os.getenv("LEMONSLICE_AVATAR_ID")
            # await lemonslice_sdk.animate(event.text, avatar_id=avatar_id)

async def main():
    # 1. API Key Validation
    required_keys = ["OPENAI_API_KEY", "STREAM_API_KEY", "STREAM_API_SECRET"]
    for key in required_keys:
        if not os.getenv(key):
            print(f"❌ Error: {key} is missing from your .env file.")
            return

    # 2. Initialize the Agent
    agent = Agent(
        edge=getstream.Edge(
            api_key=os.getenv("STREAM_API_KEY"),
            api_secret=os.getenv("STREAM_API_SECRET"),
            provide_audio=False, 
            provide_video=False,
            session_id="rudi-poc-test" # Connects to the same room as test_rudi.py
        ),
        agent_user=User(name="Rudi", id="rudi-bot"),
        instructions="You are Rudi, a helpful AI assistant. Keep responses brief.",
        llm=openai.Realtime(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini"
        ),
        processors=[LemonSliceProcessor()]
    )
    
    print("🚀 Rudi is LIVE and listening in room: rudi-poc-test")
    
    # 3. Execution with explicit Event Handling
    try:
        # We use a task to handle the safety timeout
        timeout_task = asyncio.create_task(asyncio.sleep(900))
        
        # This keeps the agent's internal listeners active
        # We wait until the timeout task finishes or we hit Ctrl+C
        await timeout_task
        print("\n🛑 Safety Timeout Reached (15 mins).")
            
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        print("\n🛑 Manual Shutdown...")
    finally:
        await agent.close()
        print("✅ Session closed securely.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"⚠️ Runtime Error: {e}")