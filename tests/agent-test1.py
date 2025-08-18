import asyncio
import os
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import requests

# --- LangSmith Configuration ---
# Set up LangSmith environment variables
# Make sure you have LANGCHAIN_API_KEY in your .env file
load_dotenv(override=True)

# Ensure LangSmith tracing is enabled
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "pr-roasted-kettledrum-85")

# --- Step 1: Setup Gemini LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

@tool
def fetch_pokemon_data(name: str) -> str:
    """Use this to fetch data about a Pokémon when given its name or ID"""
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Return only some relevant info
        info = "Name: {}\n".format(data['name'].title())
        info += "ID: {}\n".format(data['id'])
        info += "Height: {}\n".format(data['height'])
        info += "Weight: {}\n".format(data['weight'])
        info += "Base Experience: {}\n".format(data['base_experience'])
        info += "Abilities: {}\n".format([a['ability']['name'] for a in data['abilities']])
        info += "Types: {}\n".format([t['type']['name'] for t in data['types']])
        return info
    else:
        return f"Pokémon '{name}' not found."

tools = [fetch_pokemon_data]

query = "What do you know about ditto?"

# Proper implementation of ChatPromptTemplate with agent_scratchpad
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You have access to a Pokémon API. You are required to answer only using the information from the API. Respond with the relevant Pokémon data in markdown format. Be conversational and engaging."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# --- Step 3: Create the Agent ---
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

# --- Step 4: Ask the agent (async version) ---
async def run_agent():
    result = await agent_executor.ainvoke({"input": query})
    print("Final Answer:")
    print(result["output"])

    # Let's examine what's actually in the result
    print("\nKeys in result:", list(result.keys()))

    # The agent_scratchpad is internal to the agent's operation and is not directly accessible in the final output
    # It contains the intermediate steps (thoughts and tool calls) that the agent made during processing
    if "intermediate_steps" in result:
        print("\nIntermediate Steps (Agent Scratchpad):")
        for i, step in enumerate(result["intermediate_steps"]):
            print(f"\nStep {i+1}:")
            print(f"Tool: {step[0].tool}")
            print(f"Tool Input: {step[0].tool_input}")
            print(f"Tool Output: {step[1]}")
    else:
        print("\nNo intermediate steps found in the result.")
        print("Full result:", result)

# Run the async function
if __name__ == "__main__":
    asyncio.run(run_agent())