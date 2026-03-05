#!/usr/bin/env bash
set -o errexit # Exit immediately if a command exits with a non-zero status.

# Ensure commands run from this script's directory, whatever Render's current dir is.
cd "$(dirname "$0")"

pip install -r requirements.txt
python manage.py collectstatic --no-input --settings=waldo.settings
