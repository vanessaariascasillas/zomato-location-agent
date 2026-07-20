#!/bin/bash
# Adapted from the GeeksforGeeks "Location Intelligence ADK Agent" walkthrough
# for the Zomato restaurants agent instead of the original bakery example.
#
# Review the API list below before running; confirm PROJECT_ID is already
# exported (see README step 2) and that billing is enabled on that project.

set -e

if [ -z "$PROJECT_ID" ]; then
  echo "PROJECT_ID is not set. Run: export PROJECT_ID=\$(gcloud config get project)"
  exit 1
fi

echo "Enabling required APIs on project: $PROJECT_ID"
gcloud services enable \
  bigquery.googleapis.com \
  maps-backend.googleapis.com \
  places-backend.googleapis.com \
  aiplatform.googleapis.com \
  --project="$PROJECT_ID"

ENV_FILE="../adk_agent/zomato_agent/.env"

if [ -f "$ENV_FILE" ]; then
  echo "$ENV_FILE already exists, not overwriting. Edit it by hand if needed."
else
  echo "Creating $ENV_FILE from template."
  cp ../adk_agent/zomato_agent/.env.example "$ENV_FILE"
  sed -i "s/GOOGLE_CLOUD_PROJECT=.*/GOOGLE_CLOUD_PROJECT=$PROJECT_ID/" "$ENV_FILE"
  echo "Fill in MAPS_API_KEY manually in $ENV_FILE (create one in the Google Cloud Console under APIs & Services > Credentials)."
fi

echo "Done. Next: run setup_bigquery.sh"
