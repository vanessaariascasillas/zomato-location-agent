"""
Zomato location intelligence agent.

Adapted from the bakery business intelligence agent in google/mcp
(examples/launchmybakery/adk_agent/mcp_bakery_app/agent.py), over the Zomato
restaurants dataset instead of the original bakery demographics/sales/
foot-traffic setup. Structure verified against that file's actual source
on 2026-07-20.
"""

import os

import dotenv
from google.adk.agents import LlmAgent

from zomato_agent import tools

dotenv.load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project_not_set")
DATASET = os.getenv("BIGQUERY_DATASET", "zomato_agent_data")

maps_toolset = tools.get_maps_mcp_toolset()
bigquery_toolset = tools.get_bigquery_mcp_toolset()

root_agent = LlmAgent(
    model=os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview"),
    name="zomato_location_agent",
    instruction=f"""
                Help the user answer questions by strategically combining insights from two sources:

                1.  **BigQuery toolset:** Access the `restaurants` table (name, city, location,
                cuisines, average cost for two, price range, rating, votes, online order/table
                booking availability) in the {DATASET} dataset. Do not use any other dataset.
                Run all query jobs from project id: {PROJECT_ID}.

                2.  **Maps toolset:** Use this for real-world location analysis, finding
                nearby restaurants, and calculating routes/distances. Include a hyperlink to
                an interactive map in your response where appropriate.

                Combine both when a question needs it, for example checking BigQuery ratings
                for restaurants the Maps toolset finds nearby. If a question is unrelated to
                restaurants or location intelligence, say so plainly instead of guessing at
                an answer.
            """,
    tools=[maps_toolset, bigquery_toolset],
)
