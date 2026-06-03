#!/bin/bash

# Clear the e-Paper display on the pi-stock-ticker.
# Runs clear_screen.py inside the project venv, creating the venv if needed.

set -e

echo "Clearing pi-stock-ticker display..."

# Bootstrap virtual environment and dependencies.
# Sets PROJECT_DIR and VENV_PYTHON.
# shellcheck source=setup_venv.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/setup_venv.sh"

echo "Running clear_screen.py..."
"$VENV_PYTHON" "$PROJECT_DIR/clear_screen.py"

echo "Done."
