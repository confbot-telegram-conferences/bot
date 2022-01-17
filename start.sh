#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


echo "Starting the application"
make make-messages
echo "The language files were created."
source /app/.venv/bin/activate
echo "The virtualenv was activated"
python manage.py run_server
