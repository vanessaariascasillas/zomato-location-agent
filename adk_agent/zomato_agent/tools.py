"""
Maps and BigQuery MCP toolsets for the Zomato location intelligence agent.

Adapted from the bakery example in the GeeksforGeeks "Location Intelligence
ADK Agent" walkthrough, over the Zomato restaurants dataset instead of the
original demographics/sales/foot-traffic tables.

NOTE: the exact MCP toolset wiring below (connection details, auth) is
sketched out based on what the walkthrough showed, but hasn't been verified
against the real google/mcp example repo yet. Before running this for real,
check the current toolset classes/arguments in that repo, since MCP/ADK
APIs are still young and can shift between versions.
"""

import os


def get_maps_mcp_toolset():
    """
    Returns an MCP toolset connected to the Google Maps MCP server.

    Used for:
    - Place search (finding restaurants near a location)
    - Competitor/nearby analysis
    - Route/distance calculations

    Requires MAPS_API_KEY to be set in the environment.
    """
    maps_api_key = os.environ["MAPS_API_KEY"]

    # TODO: verify the real MCPToolset import path and connection arguments
    # against the current google/mcp example repo before running.
    from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

    return MCPToolset(
        connection_params={
            "type": "streamable_http",
            "api_key": maps_api_key,
        },
    )


def get_bigquery_mcp_toolset():
    """
    Returns an MCP toolset connected to the BigQuery MCP server, scoped to
    the zomato_agent_data.restaurants table created by
    setup/setup_bigquery.sh.

    Used for:
    - SQL execution over restaurant data
    - Cuisine/rating/cost-for-two analytics
    """
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    dataset = os.environ.get("BIGQUERY_DATASET", "zomato_agent_data")

    # TODO: verify the real MCPToolset import path and connection arguments
    # against the current google/mcp example repo before running.
    from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

    return MCPToolset(
        connection_params={
            "type": "oauth",
            "project_id": project_id,
            "dataset": dataset,
        },
    )
