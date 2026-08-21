
import asyncio
from contextlib import AsyncExitStack
import os
import sys

from dotenv import load_dotenv

from mcp_basics.core.claude import Claude
from mcp_basics.core.cli import CliApp
from mcp_basics.core.cli_chat import CliChat
from mcp_basics.mcp_client import MCPClient

load_dotenv(override=True)

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)

print("Python:", sys.executable)
print("API key loaded:", bool(os.getenv("ANTHROPIC_API_KEY")))
print("Using model:", claude_model)

async def main():
    claude_service = Claude(
        model=claude_model,
        api_key=anthropic_api_key,
    )
    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_basics/mcp_server.py"])
        if
            os.getenv("USE_UV", "0") == "1"
        else
            ("python", ["mcp_basics/mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client
        for i, server_script in enumerate(server_scripts):
                client_id = f"client_{i}_{server_script}"
                client = await stack.enter_async_context(
                    MCPClient(command="uv", args=["run", server_script])
                )
                clients[client_id] = client

        chat = CliChat(
                doc_client=doc_client,
                clients=clients,
                claude_service=claude_service,
            )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())