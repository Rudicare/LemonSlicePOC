import asyncio
from vision_agents.core import User, Agent
from vision_agents.plugins import getstream, openai
from dotenv import load_dotenv

load_dotenv()

async def run():
    # 1. Setup with a distinct session ID
    edge = getstream.Edge(session_id='tester-session-final')
    user = User(id='tester', name='Tester User')
    await edge.authenticate(user=user)
    
    call = await edge.create_call(call_id='lemon-test-1')
    agent = Agent(agent_user=user, edge=edge, llm=openai.Realtime())
    
    print("Tester: Joining room...")
    await edge.join(agent=agent, call=call)
    
    # 2. LONGER WAIT: Codespaces needs time to bridge the terminals
    print("Waiting 15 seconds for WebRTC bridge to stabilize...")
    await asyncio.sleep(15)
    
    print("Sending 'ping' signal via agent.say()...")
    await agent.say("ping")
    print("Signal Sent! Check Terminal 1.")

if __name__ == "__main__":
    asyncio.run(run())