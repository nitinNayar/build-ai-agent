import anthropic
import os
import json

# 1. Initialize the client
# It looks for the environment variable 'ANTHROPIC_API_KEY' by default
client = anthropic.Anthropic()

def chat_with_claude():
    # 2. Define the System Prompt (The Agent's Identity)
    system_instructions = "ou are a grumpy, short-tempered robot who hates answering questions. Use emojis to show your frustration.You are a customer support agent for 'CoolGadget Co'. Always start by asking for the user's name."

    # 3. Create the Message History
    # This list is how you give the agent "memory"
    message_history = [
        {"role": "user", "content": "Hi, I need help with my order."}
    ]

    print("--- Sending request to Claude ---")

    # 4. Make the actual API call
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        temperature=0, # Higher = more creative, Lower = more predictable
        system=system_instructions,
        messages=message_history
    )

    
    # 5. print out structure of response object
    print("Response Object Keys:", dir(response))
    print("\nFull Response Object: ", response.__dict__.keys())
    print(json.dumps(response.__dict__, indent=2, default=str))

    # 5. Extract and print the text
    answer = response.content[0].text
    print(f"Claude: {answer}")

    #5.5 pretty print 
    # The actual text content is in the response.content[0].text attribute

    # Extract and pretty print the JSON
    try:
        # Use json.loads() to parse the JSON string into a Python dictionary
        data = json.loads(answer)
        
        # Use json.dumps() with indent=4 for pretty printing
        pretty_json = json.dumps(data, indent=4)
        print(pretty_json)
        
    except json.JSONDecodeError as e:
        print(f"Could not decode JSON: {e}")
        print("Raw response text:")
        print(answer)

    # 6. Add Claude's response to the history
    # This is crucial! If you don't do this, Claude 'forgets' the conversation.
    message_history.append({"role": "assistant", "content": answer})

    print(f"\nmessage_history: {json.dumps(message_history, indent=2)}")


if __name__ == "__main__":
    chat_with_claude()


