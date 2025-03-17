from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from tools.auth import login, logout

# Initialize FastMCP server
mcp = FastMCP("google")

# Add tools
mcp.add_tool(login)
mcp.add_tool(logout)

if __name__ == "__main__":
    # Initialize and run the local stdio server
    mcp.run(transport="stdio")
