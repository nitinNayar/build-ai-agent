import anthropic
import os

# IMPORT YOUR TOOLS HERE
from day2_tools import WEATHER_TOOL_SCHEMA

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[WEATHER_TOOL_SCHEMA], # This tells Claude the tool exists!
    messages=[{"role": "user", "content": "What is the weather like in Paris?"}]
)

# Look at the 'stop_reason'
print(f"Stop Reason: {response.stop_reason}")

# Look at the 'content'
for content in response.content:
    if content.type == "tool_use":
        print(f"\nClaude wants to use a tool!")
        print(f"Tool Name: {content.name}")
        print(f"Arguments: {content.input}")