#!/bin/bash
# Tears down the resources created by setup_bigquery.sh.
# Run this when done experimenting, so nothing keeps costing money.

set -e

if [ -z "$PROJECT_ID" ]; then
  echo "PROJECT_ID is not set. Run: export PROJECT_ID=\$(gcloud config get project)"
  exit 1
fi

DATASET="zomato_agent_data"

echo "Deleting BigQuery dataset: $DATASET (and all tables in it)"
bq rm -r -f -d "$PROJECT_ID:$DATASET"

echo "Done. Also worth checking the Google Cloud Console billing page to confirm no other resources were left running."
