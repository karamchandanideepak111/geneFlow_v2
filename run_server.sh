#!/bin/bash
set -e  # Exit on any error

# Activate virtual environment
# source venv/bin/activate

# Run the Django development server
python manage.py runserver 0.0.0.0:8000 --noreload
