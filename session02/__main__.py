import os
import sys
from pathlib import Path

import anyio
import anthropic
from mcp import Client, StdioServerParameters

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
WORKING_DIR = Path(__file__).resolve().parent.parent


def load_env_file(path: Path = ENV_FILE) -> None:
    for line in path.read_text().splitlines():
        line = line.strip()
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


async def main() -> int:
    load_env_file()

    prompt = " ".join(sys.argv[1:]).strip()
    api_key = os.getenv("CLAUDE_API_KEY")

    client = anthropic.Anthropic(api_key=api_key)

    conversation = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    filesystem = StdioServerParameters(
      command = "npx",
      args = ["-y", "@modelcontextprotocol/server-filesystem", str(WORKING_DIR)]
    )

    notion = StdioServerParameters(
      command = "npx",
      args = ["-y", "@notionhq/notion-mcp-server"],
      env = {"NOTION_TOKEN": os.getenv("NOTION_TOKEN", "")}
    )


    async with Client(filesystem) as fs, Client(notion) as notion:
        tools = []
        route = {}
        for session in (fs, notion):
            for tool in (await session.list_tools()).tools:
                route[tool.name] = session
                tools.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.input_schema
                })

        while True:
            response = client.messages.create(
                model = "claude-opus-5",
                max_tokens = 5000,
                messages = conversation,
                tools = tools
            )

            conversation.append({
                "role": "assistant",
                "content": response.content
            })

            results = []
            if response.stop_reason == "tool_use":
                for block in response.content:
                    if block.type == "tool_use":
                        outcome = await route[block.name].call_tool(block.name, block.input)
                        text = "/n".join(
                            part.text for part in outcome.content if getattr(part, "text", None)
                        )
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": text
                        })

            else:
                for block in response.content:
                    if block.type == "text":
                        print(block.text)
                        return

            conversation.append({
                "role": "user",
                "content": results
            })

if __name__ == "__main__":
    anyio.run(main)