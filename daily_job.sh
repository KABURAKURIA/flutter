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

echo "Archiving generated apps..."
ZIP_FILE="${TARGET_DIR}.zip"
rm -f "$ZIP_FILE"
zip -rq "$ZIP_FILE" "$TARGET_DIR"

echo "Validating archive..."
unzip -t "$ZIP_FILE"

echo "Cleaning up source directory..."
rm -rf "$TARGET_DIR"

echo "Done. Apps created in $TARGET_DIR and archived to $ZIP_FILE"
