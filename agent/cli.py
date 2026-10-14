"""Command-line entrypoint."""
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from .graph import build_agent


def main():
    load_dotenv()
    agent = build_agent()
    print("Local Data Analyst — type 'exit' to quit")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        try:
            result = agent.invoke({"messages": [HumanMessage(content=question)]},
                                  config={"recursion_limit": 15})
            print("\nAgent:", result["messages"][-1].content)
        except Exception as exc:
            print(f"Agent error: {exc}")


if __name__ == "__main__":
    main()
