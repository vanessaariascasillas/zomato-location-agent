#!/bin/bash
# Tears down the resources created by setup_env.sh and setup_bigquery.sh.
# Adapted from the real launchmybakery cleanup_env.sh, verified against
# that source on 2026-07-20 (dropped the storage-bucket step, since this
# project's setup never creates one).

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="$SCRIPT_DIR/../adk_agent/zomato_agent/.env"
DATASET="zomato_agent_data"

if [ -f "$ENV_FILE" ]; then
  PROJECT_ID=$(grep -E "^GOOGLE_CLOUD_PROJECT=" "$ENV_FILE" | cut -d'=' -f2)
fi

if [ -z "$PROJECT_ID" ]; then
  PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
fi

if [ -z "$PROJECT_ID" ]; then
  echo "Error: could not determine Google Cloud Project ID."
  exit 1
fi

echo "----------------------------------------------------------------"
echo "CLEANUP TARGETS"
echo "----------------------------------------------------------------"
echo "Project:   $PROJECT_ID"
echo "Dataset:   $DATASET"
echo "Local Env: $ENV_FILE"
echo "----------------------------------------------------------------"
echo "WARNING: this deletes the BigQuery dataset and the local .env file."
echo "The MAPS_API_KEY was created by hand in the Console (not by a"
echo "setup script), so it is NOT deleted automatically here. Delete or"
echo "restrict it yourself under APIs & Services > Credentials if done"
echo "with it."
read -p "Are you sure you want to proceed? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cleanup cancelled."
  exit 1
fi

echo "[1/3] Removing BigQuery dataset: $DATASET"
if bq show "$PROJECT_ID:$DATASET" >/dev/null 2>&1; then
  bq rm -r -f --dataset "$PROJECT_ID:$DATASET"
  echo "      Dataset removed."
else
  echo "      Dataset not found. Skipping."
fi

echo "[2/3] Removing local .env"
if [ -f "$ENV_FILE" ]; then
  rm "$ENV_FILE"
  echo "      Deleted $ENV_FILE"
else
  echo "      .env file not found. Skipping."
fi

echo "[3/3] Checking enabled APIs"
echo "----------------------------------------------------------------"
echo "The setup enabled: bigquery, maps-backend, places-backend, aiplatform."
echo "NOTE: only disable these if no other apps in this project use them."
read -p "Do you want to disable these APIs? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Disabling APIs (this may take a moment)..."
  gcloud services disable maps-backend.googleapis.com --project="$PROJECT_ID" --force
  gcloud services disable places-backend.googleapis.com --project="$PROJECT_ID" --force
  gcloud services disable bigquery.googleapis.com --project="$PROJECT_ID" --force
  gcloud services disable aiplatform.googleapis.com --project="$PROJECT_ID" --force
  echo "APIs disabled."
else
  echo "Skipping API disablement."
fi

echo "----------------------------------------------------------------"
echo "Cleanup complete. Also worth checking the Cloud Console billing"
echo "page to confirm no other resources were left running."
echo "----------------------------------------------------------------"
