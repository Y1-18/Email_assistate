#!/bin/bash

# Create necessary directories
mkdir -p static uploads templates

# Start the FastAPI application using gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT