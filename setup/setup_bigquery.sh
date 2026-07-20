#!/bin/bash
# Creates the BigQuery dataset and loads the Zomato CSV.
#
# Uses --autodetect for the schema since I haven't inspected the real CSV
# headers yet. Once the file's downloaded, it's worth checking the detected
# schema (bq show) and tightening types by hand if autodetect gets something
# wrong (a common one: "Average Cost for two" or "Votes" getting read as a
# STRING instead of an INTEGER/FLOAT).

set -e

if [ -z "$PROJECT_ID" ]; then
  echo "PROJECT_ID is not set. Run: export PROJECT_ID=\$(gcloud config get project)"
  exit 1
fi

DATASET="zomato_agent_data"
TABLE="restaurants"
CSV_PATH="../data/zomato_restaurants.csv"

if [ ! -f "$CSV_PATH" ]; then
  echo "Expected the Zomato CSV at $CSV_PATH. Download it from Kaggle first (see README) and rename/place it there."
  exit 1
fi

echo "Creating BigQuery dataset: $DATASET"
bq --location=US mk --dataset "$PROJECT_ID:$DATASET" || echo "Dataset may already exist, continuing."

echo "Loading $CSV_PATH into $DATASET.$TABLE"
# The source CSV has a handful of rows with a stray unescaped double-quote
# in the Address field (breaks strict CSV quoting). --max_bad_records lets
# bq load skip those few rows instead of failing the whole load.
bq load \
  --autodetect \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --max_bad_records=20 \
  "$PROJECT_ID:$DATASET.$TABLE" \
  "$CSV_PATH"

echo "Done. Verify in the BigQuery console: https://console.cloud.google.com/bigquery"
echo "Check the detected schema with: bq show $PROJECT_ID:$DATASET.$TABLE"
