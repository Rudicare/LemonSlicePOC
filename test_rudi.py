import asyncio
from vision_agents.plugins import getstream, openai
from vision_agents.core import User, Agent
from dotenv import load_dotenv
load_dotenv()

async def run():
    edge = getstream.Edge(session_id='lemon-test-1')
    user = User(id='tester', name='Tester')
    await edge.authenticate(user=user)
    
    # Explicitly get the same call ID
    call = await edge.create_call(call_id='lemon-test-1')
    agent = Agent(agent_user=user, edge=edge, llm=openai.Realtime())
    
    print('Joining room as Tester...')
    await edge.join(agent=agent, call=call)
    
    # CRITICAL: Wait 5 seconds to ensure the data channel is synchronized
    print('Waiting for connection to sync...')
    await asyncio.sleep(5)
    
    print('Firing Ping...')
    await edge.send_custom_event({'type': 'test.ping'})
    print('Ping Sent! Check Terminal 1.')

if __name__ == '__main__':
    asyncio.run(run())