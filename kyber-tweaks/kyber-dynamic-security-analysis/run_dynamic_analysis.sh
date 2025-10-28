#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Kyber Dynamic Security Analysis${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for SageMath
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command_exists sage; then
    echo -e "${RED}Error: SageMath not found!${NC}"
    echo "Please install SageMath first:"
    echo "  sudo apt install sagemath"
    echo "  OR"
    echo "  conda create -n sagemath sage python=3.9"
    exit 1
fi

echo -e "${GREEN}✓ SageMath found${NC}"

# Create necessary directories
echo -e "\n${YELLOW}Setting up directories...${NC}"
mkdir -p results/{tables,plots}
mkdir -p sage-scripts
mkdir -p scripts

# Check if lattice estimator is installed
if [ ! -d "estimator/lattice-estimator" ]; then
    echo -e "\n${YELLOW}Installing lattice estimator...${NC}"
    mkdir -p estimator
    cd estimator
    git clone https://github.com/malb/lattice-estimator.git
    cd ..
    echo -e "${GREEN}✓ Lattice estimator installed${NC}"
else
    echo -e "${GREEN}✓ Lattice estimator already installed${NC}"
fi

# Run tests first
echo -e "\n${YELLOW}Running system tests...${NC}"
cd scripts
python3 test_sage_connection.py
if [ $? -ne 0 ]; then
    echo -e "${RED}System tests failed! Please fix the issues before continuing.${NC}"
    exit 1
fi
cd ..

# Run the main analysis
echo -e "\n${GREEN}Starting dynamic security analysis...${NC}"
echo -e "${YELLOW}This may take several minutes as we're computing actual security estimates${NC}"

cd scripts
python3 dynamic_analyzer.py | tee ../results/dynamic_analysis_log.txt

# Check if analysis was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Analysis completed successfully!${NC}"
    
    # Generate visualizations
    echo -e "\n${YELLOW}Generating visualizations...${NC}"
    python3 visualize_dynamic.py
    
    # Compare with static results if available
    if [ -f "../../kyber-security-analysis/results/security_analysis_results.txt" ]; then
        echo -e "\n${YELLOW}Comparing with static results...${NC}"
        python3 compare_results.py ../results/complete_results.json > ../results/comparison.txt
        echo -e "${GREEN}Comparison saved to results/comparison.txt${NC}"
    fi
    
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${GREEN}Dynamic Analysis Complete!${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "\nResults saved in:"
    echo -e "  ${BLUE}Tables:${NC} results/tables/"
    echo -e "  ${BLUE}Plots:${NC} results/plots/"
    echo -e "  ${BLUE}Raw data:${NC} results/complete_results.json"
    echo -e "  ${BLUE}Log:${NC} results/dynamic_analysis_log.txt"
else
    echo -e "\n${RED}Analysis failed! Check the log for errors.${NC}"
    exit 1
fi