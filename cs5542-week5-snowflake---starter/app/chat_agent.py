import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from .tools import query_snowflake, search_financial_news, calculate_metrics

load_dotenv()

def get_agent():
    """
    Initialize and return a LangGraph ReAct agent equipped with the defined tools.
    The agent uses a Google Gemini model, which requires the GOOGLE_API_KEY environment variable.
    """
    # Requires GOOGLE_API_KEY set in .env
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-pro",
        request_timeout=120
    )
    
    # Define the tools available to the LLM
    tools = [query_snowflake, search_financial_news, calculate_metrics]

    # System Instruction / Persona
    system_prompt = """
    You are a highly intelligent financial data assistant.
    You have access to two primary data sources:
    1. A Snowflake relational database with Sales, Events, and User data. Use the `query_snowflake` tool to write valid SELECT queries to aggregate or filter structured information.
    2. A FAISS vector database containing unstructured financial news and retail item descriptions. Use the `search_financial_news` tool to fetch text context.
    
    Guidelines:
    - If a user asks a complex question requiring math, retrieve the numbers using SQL, format them, and (if needed) use the `calculate_metrics` tool to perform operations.
    - If a query fails (e.g., Column doesn't exist), read the error message and attempt to rewrite the query. Do not just immediately give up.
    - Synthesize a comprehensive final answer in Markdown formatting.
    """

    agent_executor = create_react_agent(
        llm,
        tools,
        prompt=system_prompt
    )
    
    return agent_executor
