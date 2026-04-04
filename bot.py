import asyncio
from vision_agents.core import Agent, User
from vision_agents.plugins import getstream, openai
from dotenv import load_dotenv
import os

load_dotenv()

async def run():
    edge = getstream.Edge(session_id='lemon-test-1')
    user = User(id='rudi', name='Rudi Bot')
    await edge.authenticate(user=user)
    
    # This must be indented 4 spaces
    async def h_async(e):
        print(f'>>> EVENT RECEIVED: {e.get("type")}')
    
    # This must also be indented 4 spaces
    edge.events.subscribe(h_async)
    
    call = await edge.create_call(call_id='lemon-test-1')
    agent = Agent(agent_user=user, edge=edge, llm=openai.Realtime())
    
    print("Joining call...")
    await edge.join(agent=agent, call=call)
    
    print('--- BOT IS LIVE AND LISTENING ---')
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run())