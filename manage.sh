#!/bin/bash
# Requires the database to be up
FLASK_ENV=development DATABASE_URI=postgresql://user:password@db-service/dbname python manage.py
