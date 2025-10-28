#!/bin/bash

echo "Setting up Kyber Security Analysis..."

# Create directory structure
mkdir -p scripts results/plots

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install numpy matplotlib pandas tabulate

echo "Setup complete! Now:"
echo "1. Add your Python scripts to the scripts/ directory"
echo "2. Run: ./run_all_analysis.sh"