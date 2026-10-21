
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:8000/mcp"


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            tests = [
                ("ask_about_project", {}),
                ("search_knowledge", {"query": "Alexa"}),
                (
                    "ask_documents",
                    {
                        "question": (
                            "How many characters is each text chunk?"
                        )
                    },
                ),
            ]

            for name, arguments in tests:
                available = [tool.name for tool in tools.tools]

                if name not in available:
                    print(f"\nTool '{name}' is not registered.")
                    continue

                result = await session.call_tool(name, arguments)
                print(f"\nTool: {name}")

                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
