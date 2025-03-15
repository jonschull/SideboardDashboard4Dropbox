#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Open browser to the server URL
open http://localhost:7531

# Start the server
python3 http_server_nocache.py
python3 "$SCRIPT_DIR/http_server_nocache.py"
