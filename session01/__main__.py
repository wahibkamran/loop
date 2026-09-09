import os
import sys
from pathlib import Path

import anthropic
from session01.tavily import web_search

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def load_env_file(path: Path = ENV_FILE) -> None:
    for line in path.read_text().splitlines():
        line = line.strip()
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def main() -> int:
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

    tools = [
        {
            "name": "web_search",
            "description": "Real-time search given a prompt",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The prompt to search on"
                    }
                },
                "required": ["query"]
            }
        }
    ]

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
                if block.name == "web_search":
                    tool_result = web_search(block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_result)
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

    response = client.messages.create(
        model = "claude-opus-5",
        max_tokens = 5000,
        messages = conversation,
        tools = tools
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)
            return

if __name__ == "__main__":
    sys.exit(main())