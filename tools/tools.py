# tools.py

def get_customer_tier(email: str):
    """The actual logic: No AI here, just pure Python."""
    data = {"alice@example.com": "Gold", "bob@example.com": "Silver"}
    return data.get(email, "Standard")

def get_order_status(order_id: str):
    """Another tool for your support agent."""
    orders = {"ORD-101": "Shipped", "ORD-102": "Pending"}
    return orders.get(order_id, "Order ID not found")

# The Tool Schemas (The 'Instruction Manuals' for Claude)
# We store them in a list for easy importing
TOOL_SCHEMAS = [
    {
        "name": "get_customer_tier",
        "description": "Get loyalty tier by email.",
        "input_schema": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"]
        }
    },
    {
        "name": "get_order_status",
        "description": "Get the status of a specific order ID.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"]
        }
    }
]

# The Map: Connects the name Claude sees to the function Python runs
TOOL_MAP = {
    "get_customer_tier": get_customer_tier,
    "get_order_status": get_order_status
}