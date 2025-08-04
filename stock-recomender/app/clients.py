from langchain_mcp_adapters.client import MultiServerMCPClient
from config import Config

def get_mcp_client():
    return MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": Config.BRIGHT_DATA_API_TOKEN,
                    "WEB_UNLOCKER_ZONE": Config.WEB_UNLOCKER_ZONE,
                    "BROWSER_ZONE": Config.BROWSER_ZONE
                },
                "transport": "stdio",
            },
        }
    )