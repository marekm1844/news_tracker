#!/bin/bash

# Activate virtual environment if using one
# source /path/to/venv/bin/activate


# Start the application with Gunicorn
poetry run gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile - \
    --error-logfile - 