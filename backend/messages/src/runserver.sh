#! /usr/bin/env bash

# Start the App Server
# uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
gunicorn --workers 4 --bind 0.0.0.0:8051 -k uvicorn.workers.UvicornWorker --reload app.main:app 
