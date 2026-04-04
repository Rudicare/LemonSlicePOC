import asyncio
import os
import traceback
from dotenv import load_dotenv
from vision_agents.core import User, Agent
from vision_agents.plugins import getstream, openai

load_dotenv()

async def test_rudi():
    session_id = "rudi-poc-session-001"
    edge = getstream.Edge(session_id=session_id)
    llm = openai.Realtime()
    
    test_user = User(id="test-human", name="Tester")
    rudi_user = User(id="rudi", name="Rudi Bot")
    rudi_agent = Agent(agent_user=rudi_user, edge=edge, llm=llm)
    
    try:
        print(f"👤 Authenticating as {test_user.id}...")
        await edge.authenticate(user=test_user)
        
        print(f"📞 Joining session: {session_id}...")
        call = await edge.create_call(call_id=session_id)
        await edge.join(agent=rudi_agent, call=call)
        
        # Essential: Wait for the connection to fully open
        await asyncio.sleep(2)

        prompt = "Hello Rudi! Can you tell me a joke?"
        print(f"✉️  Sending Prompt: '{prompt}'")

        # The specific event format the Agent needs to 'hear' the message
        await edge.send_custom_event({
            "type": "message.new",
            "message": {
                "text": prompt,
                "user": {"id": "test-human", "name": "Tester"}
            }
        })

        print("⏳ Message sent! Check Terminal 1 for DEBUG logs...")
        await asyncio.sleep(5)

    except Exception:
        print("❌ TESTER ERROR:")
        traceback.print_exc()
    finally:
        await edge.close()
        print("✅ Tester session closed.")

if __name__ == "__main__":
    asyncio.run(test_rudi())