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

---

## Running Locally on Windows (VS Code)

The steps above were written for Cloud Shell and have now been run there successfully. This section covers running the same project locally instead, in VS Code on Windows, where a few things differ enough to be worth their own steps.

### Prerequisites

- **Use a Git Bash terminal**, not PowerShell or Command Prompt. Every command in this README is a bash command (`export`, `./script.sh`, etc.). Git Bash comes bundled with Git for Windows, VS Code will list it as a terminal profile (click the dropdown next to the `+` in the terminal panel) if Git is already installed, no separate install needed.
- `gcloud` and `bq` CLIs installed and authenticated (`gcloud auth login`), same as Cloud Shell but on your own machine

### The `bq` Python path issue

On Windows, `bq` may fail with an error like `python3.14: command not found` (the exact version number matches your installed Python). It's trying to invoke a version-specific Python executable name that doesn't exist on Windows (only `python.exe` does). Fix by pointing it at your real Python install before running any `bq` step:

```bash
export CLOUDSDK_PYTHON="C:/Python314/python.exe"   # adjust to your actual Python path, check with: where python
```

### Kaggle credentials, locally

Same token-based flow as Cloud Shell (see step 1 above and the Learning Log for why it's a token, not a `kaggle.json` file), just set up on your own machine instead:

```bash
mkdir -p ~/.kaggle
echo YOUR_TOKEN_HERE > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```

`~` resolves correctly in Git Bash to your Windows user profile folder, no path translation needed.

### Venv activation path differs

Windows venvs put executables in `Scripts/` instead of `bin/`:

```bash
python -m venv .venv
source .venv/Scripts/activate   # not .venv/bin/activate like Cloud Shell/Linux/Mac
pip install google-adk mcp
```

`mcp` needs to be installed separately from `google-adk`, newer ADK versions don't pull it in automatically even though MCP toolset support depends on it, same issue whether running locally or in Cloud Shell.

### Running the agent

Same as step 5 above:

```bash
cd adk_agent
adk web --allow_origins 'regex:https://.*\.cloudshell\.dev'
```

The `--allow_origins` flag is only needed in Cloud Shell, harmless to leave in locally too. Open `http://127.0.0.1:8000` in your browser.

**Finding and killing a stuck process on Windows**, if a later run fails with "address already in use":

```bash
netstat -ano | findstr :8000
taskkill //PID <pid> //F
```

Everything else (the Maps API key setup, the BigQuery load, cleanup) is identical to the Cloud Shell steps above, nothing else about them is Windows-specific.
