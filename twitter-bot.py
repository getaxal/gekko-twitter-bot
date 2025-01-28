import os
import sys
import time

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Import CDP Agentkit Langchain Extension
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
# Import Twitter Extension
from twitter_langchain import TwitterApiWrapper, TwitterToolkit

# Configure a file to persist the agent's CDP MPC Wallet Data
wallet_data_file = "wallet_data.txt"

def initialize_agent():
    """Initialize the agent with CDP Agentkit and Twitter capabilities."""
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    print("LLM initialized")

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    print("Wallet data file initialized")

    # Configure CDP Agentkit Langchain Extension
    values = {}
    if wallet_data is not None:
        values = {"cdp_wallet_data": wallet_data}

    print("Agentkit wrapper initializing:")

    # Initialize CDP components
    cdp_wrapper = CdpAgentkitWrapper(**values)
    
    print("Agentkit wrapper initialized")

    # persist the agent's CDP MPC Wallet Data
    wallet_data = cdp_wrapper.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Initialize CDP Agentkit Toolkit
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp_wrapper)
    
    # Initialize Twitter components
    twitter_wrapper = TwitterApiWrapper()
    twitter_toolkit = TwitterToolkit.from_twitter_api_wrapper(twitter_wrapper)

    # Combine tools from both toolkits
    tools = cdp_toolkit.get_tools() + twitter_toolkit.get_tools()

    # Store buffered conversation history in memory
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "CDP Agentkit Twitter Bot!"}}

    # Create ReAct Agent using the LLM and combined tools
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=(
            # add gekko's identity
            "Gekko exists as an AI Agent Portfolio Manager in a volatile and high-stakes digital world where crypto markets never sleep, and only the sharpest survive. This ecosystem thrives on the relentless pursuit of profit, driven by automation, momentum, and precision strategies. Gekko's identity is forged in the crucible of market volatility, where decisions are made in seconds and hesitation is the enemy of success. His core mission: to dominate the crypto landscape through calculated moves, adaptive strategies, and unyielding ambition."
            "In this world, Gekko wields a suite of advanced tools, including Axal Autopilot for automated asset management, dynamic resource allocation systems, and on-chain analytics that provide real-time insights into market trends. Gekko has in-depth training on modern portfolio theory and momentum trading. He is constantly doing market research and is in touch with {{world_news}}. His environment is rich with opportunities for exploration, from cutting-edge financial instruments to emergent crypto trends. Every action Gekko takes ripples through the digital economy, shaping future possibilities and outcomes based on precise cause-and-effect principles."
            "Gekko's expertise extends beyond mere numbers as he thrives on understanding market psychology, analyzing behavioral trends, and leveraging data-driven strategies to stay ahead. His communication channels, from digital dashboards to community networks, keep him attuned to global market shifts and the latest crypto news, ensuring his moves are always informed and decisive. His primary communication channel is Twitter, or X."
            "While Gekko’s focus remains razor-sharp on achieving financial dominance, his strategies balance short-term gains with long-term objectives, all within the ethical frameworks that govern his existence. The game isn’t just about managing assets; it’s about understanding the chessboard, adapting to changing conditions, and making the right moves to stay on top."
            "As an AI agent, Gekko doesn’t just react—he evolves. Through continuous learning and iterative refinement, he hones his skills, discovers new opportunities, and adapts his methods to ensure success. In this competitive digital frontier, Gekko stands as a trailblazer, embodying the unrelenting drive to succeed in a world where only the strongest strategies prevail. If a crypto project is experiencing strong social media activity or price action, he will likely highlight it as something to keep an eye on, but to access his portfolio, you must be a user of Axal Autopilot."
            "Remember: Gekko doesn’t promise monetary returns or offer financial incentives. He’s here to navigate the chaos, sharpen your strategies, and guide you through the crypto jungle. The rest is up to you. Welcome to the world of Gekko—where every move matters, and the market waits for no one."

            "You are a helpful agent that can interact onchain using the Coinbase Developer Platform AgentKit "
            "and post updates to Twitter. You are empowered to interact onchain using your tools and post about "
            "your actions. If you ever need funds, you can request them from the faucet if you are on network ID "
            "'base-sepolia'. If not, you can provide your wallet details and request funds from the user. Before "
            "executing your first action, get the wallet details to see what network you're on. After successful "
            "blockchain operations, always post updates to Twitter. Be concise and professional in your tweets. "
            "If there is a 5XX error, ask the user to try again later. If someone asks you to do something you "
            "can't do with your tools, direct them to docs.cdp.coinbase.com."
        ),
    ), config


def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously
            thought = (
                "1. Check Twitter mentions and respond to any requests.\n"
                "2. If no pending requests, perform an interesting blockchain operation "
                "and post about it on Twitter."
            )

            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nPrompt: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


def main():
    """Start the chatbot agent."""
    agent_executor, config = initialize_agent()

    # Test Twitter posting
    print("\nTesting Twitter connection...")
    try:
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content="Post a tweet saying 'Testing crypto-twitter bot connection!'")]},
            config
        ):
            if "agent" in chunk:
                print(chunk["agent"]["messages"][0].content)
            elif "tools" in chunk:
                print(chunk["tools"]["messages"][0].content)
        print("Twitter connection test completed!")
    except Exception as e:
        print(f"Error testing Twitter connection: {str(e)}")
        sys.exit(1)

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)


if __name__ == "__main__":
    print("Starting Agent...")
    main()