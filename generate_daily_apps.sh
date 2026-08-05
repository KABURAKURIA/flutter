#!/bin/bash

# Remove existing zip if any
rm -f daily_apps.zip

# Create initial 60 apps
echo "Creating initial 60 apps..."
python3 generate_apps.py 60 daily_apps

# Create 1 more app, ensuring no repeats
echo "Creating 1 additional app (daily update)..."
python3 generate_apps.py 1 daily_apps

# Archive and clean up
echo "Archiving to daily_apps.zip and cleaning up..."
zip -rq daily_apps.zip daily_apps
rm -rf daily_apps

echo "Done. Apps archived in daily_apps.zip"
