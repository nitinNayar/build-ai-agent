# --- day2_tools.py ---

# 1. The actual logic (The "Action")
# # This is a standard Python function. Claude CANNOT see this yet.
def get_weather(location: str, unit: str = "celsius"):
    """Fetches the weather for a given city."""
    # In a real app, this would call an API. For now, it's a mock.
    return f"The weather in {location} is 22 degrees {unit}."

# 2. The definition (The "Contract")
WEATHER_TOOL_SCHEMA = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
            },
        },
        "required": ["location"],
    },
}

# 3. A list of all tools in this file for easy importing
SUPPORT_TOOLS = [WEATHER_TOOL_SCHEMA]