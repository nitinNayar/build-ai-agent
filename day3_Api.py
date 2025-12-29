from config import AI_MODEL, SYSTEM_PROMPT
import anthropic
import json
from tools.tools import TOOL_SCHEMAS, TOOL_MAP 

client = anthropic.Anthropic()

class SupportAgent:
    def __init__(self):
        # This is the "Brain's Memory Bank"
        self.messages = []
        self.system_prompt = SYSTEM_PROMPT

    def ask(self, user_input):
        # 1. Add the new user message to memory
        self.messages.append({"role": "user", "content": user_input})

        # 2. Call Claude with the FULL history
        response = client.messages.create(
            model=AI_MODEL,
            max_tokens=1000,
            system=self.system_prompt,
            tools=TOOL_SCHEMAS,
            messages=self.messages
        )

        # 2.5 print out structure of response object
        print("[Internal Log] Response Object Keys:", dir(response))
        print("\n [Internal Log] Full Response Object: ", response.__dict__.keys())
        print(json.dumps(response.__dict__, indent=2, default=str))

        # 3. Handle Tool Use (The Loop)
        # Note: In a real agent, this would be a 'while' loop 
        # to handle multiple tool calls in a row!
        if response.stop_reason == "tool_use":
            tool_use = next(block for block in response.content if block.type == "tool_use")
            
            # Execute Python Tool
            tool_func = TOOL_MAP[tool_use.name]
            result = tool_func(**tool_use.input)

            print(f"[Internal Log] Agent called {tool_use.name} with {tool_use.input}")
            print(f"[Internal Log] Result: {result}")

            # Add BOTH Claude's thought and the result to memory
            self.messages.append({"role": "assistant", "content": response.content})
            self.messages.append({
                "role": "user", 
                "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": str(result)}]
            })

            # Call Claude again to get the final "verbal" answer
            final_response = client.messages.create(
                model=AI_MODEL,
                max_tokens=1000,
                system=self.system_prompt,
                tools=TOOL_SCHEMAS,
                messages=self.messages
            )

            # 2.5 print out structure of response object
            print("[Internal Log] Response Object Keys:", dir(response))
            print("\n [Internal Log] Full Response Object: ", response.__dict__.keys())
            print(json.dumps(response.__dict__, indent=2, default=str))

            print(f"[Internal Log] Agent called {tool_use.name} with {tool_use.input}")
            print(f"[Internal Log] Result: {result}")

            # Add final answer to memory
            self.messages.append({"role": "assistant", "content": final_response.content})
            return final_response.content[0].text

        # If no tool was used, just save and return the answer
        self.messages.append({"role": "assistant", "content": response.content})
        return response.content[0].text

# --- RUNNING THE CHAT ---
agent = SupportAgent()

print("Agent: Hello! How can I help you today?")
while True:
    user_msg = input("You: ")
    if user_msg.lower() in ["exit", "quit"]: break
    
    answer = agent.ask(user_msg)
    print(f"Agent: {answer}")