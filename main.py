import asyncio

from ai_handler import AIHandler
from grok_collection import GrokCollection


async def main() -> None:
    handler = AIHandler(
        model="grok-3",
        system_prompt="You are a helpful Python assistant.",
    )
    collection = GrokCollection(collection_name="python_docs")

    await collection.add(
        documents=[
            "Python list comprehensions allow concise creation of lists.",
            "The walrus operator := assigns and returns a value in one expression.",
            "Type hints improve readability and enable static analysis.",
        ]
    )

    # Plain streaming chat
    print("--- Streaming ---")
    async for chunk in handler.stream("Explain list comprehensions briefly."):
        print(chunk, end="", flush=True)
    print()

    # RAG-augmented chat
    print("\n--- Chat with Context ---")
    handler.reset()
    answer = await handler.chat_with_context(
        "What is the walrus operator?",
        collection=collection,
    )
    print(answer)
    print(f"\nDocs in collection: {collection.count()}")


asyncio.run(main())
