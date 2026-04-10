#!/usr/bin/env bash
# exit on error
set -o errexit

# Log versions for debugging
python --version
pip --version

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p media
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
