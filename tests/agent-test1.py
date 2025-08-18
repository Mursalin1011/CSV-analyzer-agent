from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv
import requests

# --- Step 1: Setup Gemini LLM ---
# Make sure you have GOOGLE_API_KEY in your environment
load_dotenv(override=True)
llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "qwen3:0.6b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.1
        )

# --- Step 2: Define a Tool for Pokémon API ---
def fetch_pokemon_data(name: str) -> str:
    """Fetch basic Pokémon data from PokeAPI by name or ID."""
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Return only some relevant info
        return (
            f"Name: {data['name'].title()}\n"
            f"ID: {data['id']}\n"
            f"Height: {data['height']}\n"
            f"Weight: {data['weight']}\n"
            f"Base Experience: {data['base_experience']}\n"
            f"Abilities: {[a['ability']['name'] for a in data['abilities']]}\n"
            f"Types: {[t['type']['name'] for t in data['types']]}"
        )
    else:
        return f"Pokémon '{name}' not found."

pokemon_tool = Tool(
    name="Pokemon API",
    func=fetch_pokemon_data,
    description="Use this to fetch data about a Pokémon when given its name or ID."
)

# --- Step 3: Create the Agent ---
agent = initialize_agent(
    tools=[pokemon_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# --- Step 4: Ask the agent ---
print(agent.run("Tell me about pikachu"))
