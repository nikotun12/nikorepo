#!/bin/bash

set -e

MODE=${1:-base}

cd "$(dirname "$0")"

export OBSIDIAN_API_KEY="${OBSIDIAN_API_KEY:-test_key}"

if [ "$MODE" = "base" ]; then
    echo "Running base tests (existing functionality)..."
    python -m pytest tests/test_existing_tools.py -v
    echo "✓ Base tests passed"
    
elif [ "$MODE" = "new" ]; then
    echo "Running new feature tests (backlink discovery)..."
    python -m pytest tests/test_backlinks.py -v
    echo "✓ New tests passed"
    
else
    echo "Usage: ./test.sh [base|new]"
    echo "  base - Run tests for existing functionality"
    echo "  new  - Run tests for backlink discovery feature"
    exit 1
fi
