from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from tools.reply import reply_message
from tools.search import search_messages
from tools.send import send_message

# Initialize FastMCP server
mcp = FastMCP("email")

# Add tools
mcp.add_tool(search_messages)
mcp.add_tool(send_message)
mcp.add_tool(reply_message)

if __name__ == "__main__":
    # Initialize and run the local stdio server
    mcp.run(transport="stdio")
