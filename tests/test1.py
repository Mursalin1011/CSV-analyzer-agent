import os
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM


# ====== STEP 1: Paste your Gemini API key here ======
load_dotenv(override=True)  # Load environment variables from .env file
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" or "ollama"

# ====== STEP 2: Create sample sales data in code ======
data = {
    "Product": ["Laptop", "Smartphone", "Headphones", "Monitor", "Keyboard",
                "Mouse", "Printer", "Tablet", "Camera", "Smartwatch"],
    "Sales": [1500, 2400, 800, 1200, 600, 500, 900, 1100, 1300, 700],
    "Region": ["North", "East", "South", "West", "North",
               "East", "South", "West", "North", "East"]
}
df = pd.DataFrame(data)
print("Generated Sales Data:")
print(df, "\n")

# ====== STEP 3: Summarize/Filter for Token Saving ======
#summary_data = df.nlargest(5, 'Sales').to_string(index=False)
summary_data = df.nsmallest(5, 'Sales').to_string(index=False)

# ====== STEP 4: Create LLM (Low Temperature for Facts) ======
if LLM_PROVIDER == "gemini":
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1  # Reduced from 0.3 for more focused responses
    )
elif LLM_PROVIDER == "ollama":
    llm = OllamaLLM(
        model=os.getenv("OLLAMA_MODEL", "granite3.3:2b"),  # Get model from env or use default
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.3
        
    )
else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

# ====== STEP 5: Create Prompt Template ======
prompt = PromptTemplate(
    input_variables=["data", "question"],
    template=(
        "You are a helpful data analyst.\n"
        "Here is part of the sales data:\n{data}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
)

# ====== STEP 6: Create Chain ======
chain = prompt | llm

# ====== STEP 7: Ask Question ======
user_question = "Which product had the least sales?"
#user_question = "Which product had the highest sales?"
answer = chain.invoke({"data": summary_data, "question": user_question})

print("=== Question ===")
print(user_question)

print("===summarized data sent to llm===")
print(summary_data)

print("\n=== AI Answer ===")
print(answer)