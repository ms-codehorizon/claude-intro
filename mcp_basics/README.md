# MCP Basics

This folder contains a basic MCP server and client. The server provides tools and resources for reading and editing sample documents. The main application connects the MCP server to Claude and starts an interactive command-line chat.

## Setup

Complete the setup in the root `README.md` first. Run all commands below from the repository root.

## Run the application

```bash
uv run python -m mcp_basics.main
```

Ask a question at the prompt:

```text
What is the content of report.pdf?
```

Use `@` to load a document as a resource:

```text
What is the content of @report.pdf?
```

## Test the client

```bash
uv run python -m mcp_basics.mcp_client
```

## Open MCP Inspector

```bash
uv run mcp dev mcp_basics/mcp_server.py
```

The Inspector command also requires Node.js and npm.
