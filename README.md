# loop

Source code for the loop session workshops. Each `sessionNN/` directory is a self-contained, runnable example from one workshop.

## Setup

1. Create a `.env` file in this directory (it is gitignored) with:

```
CLAUDE_API_KEY=your-anthropic-api-key
TAVILY_API_KEY=your-tavily-api-key      # session01
NOTION_TOKEN=your-notion-integration-secret  # session02
```

2. Install Python dependencies with `pip install -r requirements.txt`.

3. Install [Node.js](https://nodejs.org/en/download) (v18+). session02 launches its MCP servers with `npx`, which downloads them automatically on first run.

Then see each session's README to run it.
