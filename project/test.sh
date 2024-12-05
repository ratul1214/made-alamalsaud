#!/bin/bash

# Exit immediately if any command exits with a non-zero status
set -e

# Paths
DATA_DIR="/Users/alamalsaud/Projects/MadeProject"
DATABASE_PATH="$DATA_DIR/data/cleaned_data.sqlite"
CLEANED_CSV1="$DATA_DIR/cleaned_data1.csv"
CLEANED_CSV2="$DATA_DIR/cleaned_data2.csv"

# Run the pipeline script
echo "Running the data pipeline..."
python3 main.py

# Validate output files
echo "Validating output files..."
if [[ -f "$CLEANED_CSV1" && -f "$CLEANED_CSV2" ]]; then
    echo "CSV output files are present."
else
    echo "CSV output files are missing!"
    exit 1
fi

# Validate database file
echo "Validating database file..."
if [[ -f "$DATABASE_PATH" ]]; then
    echo "Database file is present."
else
    echo "Database file is missing!"
    exit 1
fi

# Check if tables exist in the database
echo "Checking database contents..."
sqlite3 "$DATABASE_PATH" <<EOF
.tables
EOF

echo "Tests passed!"