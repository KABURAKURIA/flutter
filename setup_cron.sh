#!/bin/bash

SCRIPT_PATH="$(realpath daily_job.sh)"
CRON_JOB="0 0 * * * $SCRIPT_PATH >> $(dirname "$SCRIPT_PATH")/daily_flutter_app.log 2>&1"

# Check if the cron job already exists
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") > /dev/null
if [ $? -eq 0 ]; then
    echo "Cron job for daily_job.sh is already configured."
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Successfully configured daily cron job to run $SCRIPT_PATH."
fi
