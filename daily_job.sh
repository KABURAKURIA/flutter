#!/bin/bash

# Create a unique folder for today's run
TODAY=$(date +"%Y%m%d_%H%M%S")
TARGET_DIR="daily_apps_$TODAY"

echo "Creating new folder: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Check the global index to determine if we should generate 60 apps or 1 app
if [ -f ".global_app_index" ]; then
    echo "Global index found. Generating 1 new app for today..."
    python3 generate_apps.py 1 "$TARGET_DIR"
else
    echo "No global index found. Generating initial 60 apps..."
    python3 generate_apps.py 60 "$TARGET_DIR"
fi

echo "Done. Apps created in $TARGET_DIR"
