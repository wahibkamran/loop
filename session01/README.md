# Session 01 — Tool Use

Command to run the function:
```bash
python -m session01 "your prompt here"
```

A minimal agentic loop: send a prompt with a `web_search` tool, run the tool if Claude asks for it, feed the result back, and print the final answer.

Requires `CLAUDE_API_KEY` and `TAVILY_API_KEY` in the repo-root `.env`.

## Files

- `__main__.py` — entry point. Loads `.env`, defines the `web_search` tool, calls the Claude API, handles `tool_use`, and prints the reply.
- `tavily.py` — `web_search()`, which POSTs the query to the Tavily API and returns the title/url/content of each result as JSON.
- `__init__.py` — marks the directory as a package.