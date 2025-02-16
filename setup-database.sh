#!/bin/bash

# Check if PostgreSQL is installed
if ! command -v postgres &> /dev/null; then
    echo "Installing PostgreSQL..."
    brew install postgresql@14
    
    # Start PostgreSQL service
    brew services start postgresql@14
    
    # Wait for PostgreSQL to start
    sleep 5
fi

# Create database if it doesn't exist
DB_NAME="myappdb"
if ! psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Creating database..."
    createdb $DB_NAME
fi

echo "Database setup complete!"
