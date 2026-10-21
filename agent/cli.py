from langchain_core.messages import HumanMessage
from agent.graph import agent_graph

def main():
    print("Local AI Data Analyst")
    print("Model: Qwen3.5:9b")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            result = agent_graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=question)
                    ]
                },
                config={"recursion_limit": 20},
            )

            answer = result["messages"][-1].content
            print(f"\nAgent: {answer}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
