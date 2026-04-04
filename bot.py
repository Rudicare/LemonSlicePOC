import asyncio
import os
import traceback
import warnings
from dotenv import load_dotenv
from vision_agents.core import Agent, User
from vision_agents.core.processors import Processor
from vision_agents.plugins import getstream, openai

load_dotenv()
warnings.filterwarnings("ignore", category=RuntimeWarning, module="dataclasses_json.core")

class LemonSliceProcessor(Processor):
    def __init__(self, avatar_id):
        super().__init__()
        self.avatar_id = avatar_id
        self.allowed_user_id = "test-human"

    @property
    def name(self) -> str:
        return "LemonSliceProcessor"

    async def process(self, event):
        event_type = event.get("type")
        
        # --- NEW DEBUG CATCH-ALL ---
        # This will print every single event that passes through the processor
        print(f"DEBUG: Received event type -> {event_type}")
        
        if event_type == "agent.response.text.done":
            text_content = event.get("text", "")
            print(f"🎬 [MATCH]: AI is speaking: '{text_content[:40]}...'")
            
            await self.edge.send_custom_event({
                "type": "avatar.speak",
                "avatar_id": self.avatar_id,
                "text": text_content
            })

    async def close(self):
        pass

async def run_rudi():
    session_id = "rudi-poc-session-001"
    avatar_id = os.getenv("LEMONSLICE_AVATAR_ID", "agent_4626e3e8a3aa8937")
    
    edge = getstream.Edge(session_id=session_id)
    llm = openai.Realtime()
    ls_processor = LemonSliceProcessor(avatar_id=avatar_id)
    
    rudi_user = User(id="rudi", name="Rudi Bot")
    rudi_agent = Agent(
        agent_user=rudi_user, 
        edge=edge, 
        llm=llm,
        processors=[ls_processor]
    )

    print("🚀 Initializing Rudi...")
    try:
        await edge.authenticate(user=rudi_user)
        call = await edge.create_call(call_id=session_id)
        await edge.join(agent=rudi_agent, call=call)
        
        print(f"✅ Rudi is LIVE in: {session_id}")
        while True:
            await asyncio.sleep(1)
    except Exception:
        traceback.print_exc()
    finally:
        await edge.close()

if __name__ == "__main__":
    asyncio.run(run_rudi())