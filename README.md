# Zomato Location Intelligence Agent

A small AI agent that answers location and business questions about restaurants, using Google ADK, BigQuery, Google Maps, MCP, and Gemini.

This project is my own smaller-scale build, inspired by a GeeksforGeeks video, "Build a Location Intelligence ADK Agent with MCP servers for BigQuery and Google Maps" (unlisted on the [GeeksforGeeks YouTube channel](https://www.youtube.com/@GeeksforGeeksVideos), not publicly searchable). That walkthrough builds a bakery business intelligence agent over BigQuery demographic/sales data and the Google Maps MCP server. I'm following that same pattern (BigQuery MCP toolset, Maps MCP toolset, Gemini reasoning) but over a single, simpler dataset instead of the original multi-table bakery setup: the "Zomato Restaurants Data" dataset from Kaggle (restaurant name, location, cuisine, cost for two, ratings, across many countries).

Credit: the ADK, MCP, and Gemini pattern is from that GeeksforGeeks walkthrough and Google's own codelab/`google/mcp` example repo behind it, not something I invented. What's original here is the smaller data source and the specific questions this agent answers.

## What This Agent Answers

Example questions it should be able to handle once built:

- "What are the highest-rated Italian restaurants in Rome?"
- "What's the average cost for two in Paris compared to London?"
- "Find restaurants near [a location] that take online orders."

## Project Structure

```
zomato-location-agent/
├── data/                       # zomato_restaurants.csv lands here (not committed, see .gitignore)
├── setup/
│   ├── download_dataset.py     # Downloads the Zomato dataset via kagglehub into data/
│   ├── setup_env.sh            # Enables required GCP APIs, creates .env, configures Maps API key
│   └── setup_bigquery.sh       # Creates the BigQuery dataset/table and loads the Zomato CSV
├── cleanup/
│   └── cleanup_env.sh          # Tears down the BigQuery dataset and any created resources
└── adk_agent/
    └── zomato_agent/
        ├── agent.py             # The ADK LlmAgent definition (Gemini + both MCP toolsets)
        ├── tools.py             # Maps MCP toolset + BigQuery MCP toolset wiring
        └── .env.example         # Template for required environment variables
```

## Setup (Not Yet Run)

This is the full command sequence, in order. Nothing here has actually been run yet, this is the plan, not a confirmed working log.

### 1. Get the dataset

```bash
pip install kagglehub
python setup/download_dataset.py
```

This downloads the "Zomato Restaurants Data" dataset (shrutimehta, ~9,000 restaurants worldwide) and copies the CSV to `data/zomato_restaurants.csv`. Requires Kaggle API credentials configured first if you haven't done that before.

### 2. Set up the Google Cloud project

```bash
gcloud auth list
gcloud config get project
export PROJECT_ID=$(gcloud config get project)
```

Make sure billing is enabled on this project before continuing.

### 3. Run the environment and BigQuery setup scripts

```bash
chmod +x setup/setup_env.sh setup/setup_bigquery.sh cleanup/cleanup_env.sh
./setup/setup_env.sh
./setup/setup_bigquery.sh
```

Check the detected schema afterward, since it uses `--autodetect`:

```bash
bq show $PROJECT_ID:zomato_agent_data.restaurants
```

### 4. Fill in the .env file

`setup_env.sh` creates `adk_agent/zomato_agent/.env` from the template automatically, but `MAPS_API_KEY` still needs to be filled in by hand (create one in Google Cloud Console under APIs & Services > Credentials).

### 5. Install ADK and run the agent

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk
cd adk_agent
adk web --allow_origins 'regex:https://.*\.cloudshell\.dev'
```

Then open `http://127.0.0.1:8000` (or the Cloud Shell Web Preview on port 8000 if running this in Cloud Shell instead of a local terminal).

### 6. When done, clean up

```bash
./cleanup/cleanup_env.sh
```

This README will get updated as each of these steps actually gets run for real, including fixing anything above that turns out to be wrong.
