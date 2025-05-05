#!/bin/bash
# Helper script to run the backend server with the correct PYTHONPATH
export PYTHONPATH=backend
python backend/server/main.py "$@" 