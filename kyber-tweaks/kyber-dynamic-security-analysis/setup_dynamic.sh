#!/bin/bash

echo "Setting up Kyber Dynamic Security Analysis Environment"
echo "====================================================="

# Create directory structure
echo "Creating directory structure..."
mkdir -p {scripts,results/{tables,plots},sage-scripts,estimator}

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create requirements file
cat > requirements.txt << EOF
numpy==1.24.3
matplotlib==3.7.1
tabulate==0.9.0
EOF

# Install Python requirements
echo "Installing Python requirements..."
pip3 install -r requirements.txt

# Check for SageMath
echo ""
echo "Checking for SageMath..."
if command -v sage &> /dev/null; then
    sage_version=$(sage --version | head -n1)
    echo "Found: $sage_version"
else
    echo "SageMath not found!"
    echo ""
    echo "Please install SageMath using one of these methods:"
    echo ""
    echo "1. Using apt (Ubuntu/Debian):"
    echo "   sudo apt update && sudo apt install sagemath"
    echo ""
    echo "2. Using conda:"
    echo "   conda create -n sagemath sage python=3.9"
    echo "   conda activate sagemath"
    echo ""
    echo "3. Download from: https://www.sagemath.org/download.html"
    echo ""
    echo "After installing SageMath, run this setup script again."
    exit 1
fi

# Install lattice estimator
echo ""
echo "Installing lattice estimator..."
cd estimator
if [ ! -d "lattice-estimator" ]; then
    git clone https://github.com/malb/lattice-estimator.git
    echo "Lattice estimator cloned successfully"
else
    echo "Lattice estimator already exists"
fi
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy all the Python scripts to the scripts/ directory"
echo "2. Copy the sage script to sage-scripts/ directory"
echo "3. Run: ./run_dynamic_analysis.sh"