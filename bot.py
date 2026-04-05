import asyncio
from vision_agents.core import User, Agent
from vision_agents.plugins import getstream, openai
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("--- STARTING CODESPACE RELIABILITY DEMO ---")
    
    # 1. SETUP THE BOT (The Listener)
    bot_edge = getstream.Edge(session_id='bot-session-unique-999')
    bot_user = User(id='rudi', name='Rudi Bot')
    await bot_edge.authenticate(user=bot_user)
    
    # Track success to stop the loop
    success = False

    async def bot_handler(e):
        nonlocal success
        e_type = e.get("type")
        print(f"[BOT EVENT RECEIVED] Type: {e_type}")
        
        # Check for ping in the custom data
        if "ping" in str(e).lower():
            print("\n>>> ✅ SUCCESS! BOT CAPTURED THE PING SIGNAL!")
            success = True

    bot_edge.events.subscribe(bot_handler)
    
    bot_call = await bot_edge.create_call(call_id='shared-demo-room')
    bot_agent = Agent(agent_user=bot_user, edge=bot_edge, llm=openai.Realtime())
    
    print("[BOT] Joining call...")
    await bot_edge.join(agent=bot_agent, call=bot_call)
    print("[BOT] Live and listening.")

    # 2. SETUP THE TESTER (The Sender)
    print("\n[TESTER] Initializing...")
    tester_edge = getstream.Edge(session_id='tester-session-unique-888')
    tester_user = User(id='tester', name='Tester User')
    await tester_edge.authenticate(user=tester_user)
    
    tester_call = await tester_edge.create_call(call_id='shared-demo-room')
    tester_agent = Agent(agent_user=tester_user, edge=tester_edge, llm=openai.Realtime())
    
    print("[TESTER] Joining same call...")
    await tester_edge.join(agent=tester_agent, call=tester_call)
    
    print("\n[SYSTEM] Waiting for stabilization...")
    await asyncio.sleep(10)

    # 3. LOOPING SENDER (Guarantees the Bot catches it)
    print("[TESTER] Starting Ping Loop...")
    for i in range(5):
        if success: break
        
        print(f"[TESTER] Sending Ping Attempt #{i+1}...")
        await tester_edge.send_custom_event({
            "type": "test.ping",
            "custom": {"text": "ping"}
        })
        await asyncio.sleep(5) # Give the bot time to respond

    if not success:
        print("\n[!] Timeout: Bot did not receive the ping. Check network logs.")
    
    print("\n--- DEMO COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(main())