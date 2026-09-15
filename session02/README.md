# Session 02 — MCP Servers

Command to run the function:
```bash
python -m session02 "your prompt here"
```

The same agentic loop as session01, but the tools are no longer hand-written. Instead, two [MCP](https://modelcontextprotocol.io) servers are spawned as subprocesses and every tool they expose is handed to Claude:

- **Filesystem** (`@modelcontextprotocol/server-filesystem`) — read, write, list and search files, scoped to the repo root.
- **Notion** (`@notionhq/notion-mcp-server`) — search, read and write pages/databases in a Notion workspace.

At startup the script lists the tools from each server, builds a `route` map (tool name → server session) and passes the combined tool list to Claude. When Claude returns `tool_use`, the call is forwarded to whichever server owns that tool, the result is fed back, and the loop continues until Claude replies with plain text.

## Sample prompt

```bash
python -m session02 "add documentation for session01"
```

Claude will typically call `list_directory` / `read_file` on `session01/` to understand the code, then `write_file` to create or update `session01/README.md`. Because the Notion server is also connected, you can extend the prompt, e.g. `"... and publish it to a new Notion page"`.

## Steps to run

Complete the setup in the repo-root [README](../README.md) first (`.env`, `pip install`, Node.js). Then:

1. Create a Notion integration and copy its internal integration secret into `NOTION_TOKEN` in the repo-root `.env` (see Resources below).
2. Share at least one Notion page with the integration (page `•••` menu → **Connections** → pick your integration), otherwise the Notion tools will return nothing.
3. Run `python -m session02 "your prompt here"` from the repo root.

Requires `CLAUDE_API_KEY` and `NOTION_TOKEN` in the repo-root `.env`.

## Files

- `__main__.py` — entry point. Loads `.env`, starts the filesystem and Notion MCP servers over stdio, collects their tools, runs the Claude tool-use loop and prints the reply.
- `__init__.py` — marks the directory as a package.

## Resources

- [Notion — Create an integration & get the secret](https://developers.notion.com/docs/create-a-notion-integration) — how to create an internal integration and copy the `NOTION_TOKEN`.
- [Notion — Add connections to pages](https://www.notion.so/help/add-and-manage-connections-with-the-api) — pages must be explicitly shared with the integration.
- [Notion MCP server](https://github.com/makenotion/notion-mcp-server) — the `@notionhq/notion-mcp-server` package used here and the tools it exposes.
- [Filesystem MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) — the `@modelcontextprotocol/server-filesystem` package and its allowed-directory model.
- [Model Context Protocol docs](https://modelcontextprotocol.io/introduction) — what MCP is and how servers/clients communicate.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — the `mcp` package (`Client`, `StdioServerParameters`) used to talk to the servers.
- [Claude API — Tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview) — how `tools`, `tool_use` and `tool_result` blocks work.
- [Node.js downloads](https://nodejs.org/en/download) — needed for `npx`.
