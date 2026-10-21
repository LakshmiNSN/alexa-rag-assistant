
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:8000/mcp"


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            init_result = await session.initialize()

            print(
                "MCP protocol version:",
                init_result.protocolVersion
            )

            tools = await session.list_tools()
            available_tools = [tool.name for tool in tools.tools]

            print("Available tools:", available_tools)

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
                if name not in available_tools:
                    print(f"\nTool '{name}' is not registered.")
                    continue

                result = await session.call_tool(name, arguments)

                print(f"\nTool: {name}")

                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)

                if result.isError:
                    print("Tool returned an error.")


if __name__ == "__main__":
    asyncio.run(main())

