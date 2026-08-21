# All About Claude

This repository contains basic examples for learning the Anthropic API and Model Context Protocol.

## Folders

- `claude_basics`: Notebooks and examples for using the Anthropic API.
- `mcp_basics`: A basic MCP server, MCP client, and command-line chat application.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An Anthropic API key

## First-time setup

Clone the repository and enter the project:

```bash
git clone https://github.com/ms-codehorizon/claude-intro.git all-about-claude
cd all-about-claude
```

Create the project environment and install all dependencies:

```bash
uv sync --python 3.12
```

Create a `.env` file in the repository root:

```dotenv
ANTHROPIC_API_KEY=your_api_key
CLAUDE_MODEL=claude-sonnet-4-5
USE_UV=1
```

Do not commit the `.env` file.

## Run

Run the basic project entry point:

```bash
uv run python -m claude_basics.main
```

Run the MCP chat application:

```bash
uv run python -m mcp_basics.main
```

You do not need to activate `.venv` when using `uv run`.
