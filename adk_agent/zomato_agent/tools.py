"""
Maps and BigQuery MCP toolsets for the Zomato location intelligence agent.

Adapted from the bakery example in google/mcp
(examples/launchmybakery/adk_agent/mcp_bakery_app/tools.py), verified against
that file's actual source on 2026-07-20.
"""

import os

import dotenv
import google.auth
import google.auth.transport.requests
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"
BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"


def get_maps_mcp_toolset():
    """
    Returns an MCP toolset connected to the Google Maps MCP server.

    Used for:
    - Place search (finding restaurants near a location)
    - Competitor/nearby analysis
    - Route/distance calculations

    Requires MAPS_API_KEY to be set in the environment.
    """
    dotenv.load_dotenv()
    maps_api_key = os.getenv("MAPS_API_KEY", "no_api_found")

    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MAPS_MCP_URL,
            headers={
                "X-Goog-Api-Key": maps_api_key,
            },
            timeout=30.0,
            sse_read_timeout=300.0,
        )
    )
    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools


def get_bigquery_mcp_toolset():
    """
    Returns an MCP toolset connected to the BigQuery MCP server, authenticated
    via the caller's own OAuth credentials against whichever GCP project is
    active (the one holding the zomato_agent_data.restaurants table created
    by setup/setup_bigquery.sh).
    """
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    oauth_token = credentials.token

    headers_with_oauth = {
        "Authorization": f"Bearer {oauth_token}",
        "x-goog-user-project": project_id,
    }

    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=BIGQUERY_MCP_URL,
            headers=headers_with_oauth,
            timeout=30.0,
            sse_read_timeout=300.0,
        )
    )
    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools
