#!/bin/bash

TARGET_DIR="daily_apps"
ZIP_FILE="${TARGET_DIR}.zip"

# If zip exists, unzip it so we can determine the next index and add to it
if [ -f "$ZIP_FILE" ]; then
    echo "Existing archive found. Extracting to continue..."
    unzip -q "$ZIP_FILE"
fi

if [ -d "$TARGET_DIR" ] && [ "$(ls -A "$TARGET_DIR" 2>/dev/null | grep -c 'flutter_app_')" -gt 0 ]; then
    echo "Directory exists and contains apps. Generating 1 new app..."
    python3 generate_apps.py 1 "$TARGET_DIR"
else
    echo "Directory does not exist or is empty. Generating initial 60 apps..."
    python3 generate_apps.py 60 "$TARGET_DIR"
fi

echo "Deleting old archive..."
rm -f "$ZIP_FILE"

echo "Archiving generated apps..."
zip -rq "$ZIP_FILE" "$TARGET_DIR"

echo "Validating archive..."
unzip -t "$ZIP_FILE"

echo "Cleaning up source directory..."
rm -rf "$TARGET_DIR"

echo "Done."
