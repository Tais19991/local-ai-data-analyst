import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from agent.tools import DATABASE_TOOLS
load_dotenv()

SYSTEM_PROMPT = """
You are a local AI data analyst working with PostgreSQL.

Your responsibilities:
- Answer analytical questions using actual database data.
- Discover tables and inspect their schemas before writing SQL.
- Use PostgreSQL syntax.
- Use only SELECT queries.
- Never modify database data or schema.
- Do not invent query results.
- If a query fails, inspect the error and correct it.
- Explain the final results clearly and concisely.
- For percentages, prefer ROUND(AVG(column::numeric) * 100, 2).
- PostgreSQL ROUND(value, decimals) requires NUMERIC, not DOUBLE PRECISION.
- If a SQL tool returns success=False, inspect the error and retry
  with corrected SQL.
- Never report a failed query as a successful result.
- Limit SQL correction attempts to 3 per user question.

The database contains a schema named titanic.
"""


def build_graph():
    model = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3.5:9b"),
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        temperature=0,
    )
    model_with_tools = model.bind_tools(DATABASE_TOOLS)

    def agent_node(state: MessagesState):
        response = model_with_tools.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                *state["messages"],
            ]
        )
        return {"messages": [response]}
    graph = StateGraph(MessagesState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(DATABASE_TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END,
        },
    )
    graph.add_edge("tools", "agent")
    return graph.compile()


agent_graph = build_graph()
