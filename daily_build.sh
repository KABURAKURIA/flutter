#!/bin/bash

# Target directory for daily apps
TARGET_DIR="daily_apps"

# Check if the target directory exists and is not empty
if [ -d "$TARGET_DIR" ] && [ "$(ls -A "$TARGET_DIR")" ]; then
    echo "Directory $TARGET_DIR exists. Generating 1 new app..."
    python3 generate_apps.py 1 "$TARGET_DIR"
else
    echo "Directory $TARGET_DIR does not exist or is empty. Generating initial 60 apps..."
    python3 generate_apps.py 60 "$TARGET_DIR"
fi
