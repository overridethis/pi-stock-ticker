#!/bin/bash

# Shared venv bootstrap for pi-stock-ticker.
# Source this script from other shell scripts to ensure the project venv
# exists and dependencies are installed.
#
# Exports:
#   PROJECT_DIR  - absolute path to project root
#   VENV_PYTHON  - path to venv python3
#   VENV_PIP     - path to venv pip3

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"
VENV_PIP="$PROJECT_DIR/venv/bin/pip3"

# Check if virtual environment exists, create if not
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Creating one now..."
    python3 -m venv "$PROJECT_DIR/venv"

    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure python3-venv is installed:"
        echo "  sudo apt-get install python3-venv"
        exit 1
    fi

    echo "Virtual environment created successfully."
else
    echo "Virtual environment found at $PROJECT_DIR/venv"
fi

# Always install/update dependencies
echo "Installing project dependencies..."

"$VENV_PIP" install --upgrade pip
"$VENV_PIP" install --prefer-binary -e "$PROJECT_DIR"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully."
