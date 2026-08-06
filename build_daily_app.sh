#!/bin/bash

# Directory to store the apps
OUTPUT_DIR="daily_apps"

# Check if the directory exists and contains flutter_app_* folders
if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" | grep -c 'flutter_app_')" -gt 0 ]; then
    echo "Directory exists and contains apps. Generating 1 new app..."
    python3 generate_apps.py 1 "$OUTPUT_DIR"
else
    echo "Directory does not exist or is empty. Generating initial 60 apps..."
    python3 generate_apps.py 60 "$OUTPUT_DIR"
fi
