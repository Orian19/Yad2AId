#!/bin/bash

# Activate the virtual environment
# source /home/site/wwwroot/venv/bin/activate

# Start your FastAPI app
python -m uvicorn fastApiApp.apartment_finder:app --host 0.0.0.0 --port 8000

# Set up your scheduled tasks
# python -m functions.function1 &
# python -m functions.function2 &

# Keep the container running
tail -f /dev/null
