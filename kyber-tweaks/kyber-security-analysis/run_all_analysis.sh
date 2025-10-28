#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Kyber Security Analysis (Static/Hardcoded)${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Error: Virtual environment not activated!${NC}"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Create results directories if they don't exist
mkdir -p results/plots

# 1. Run main security analysis
echo -e "\n${GREEN}1. Running main security analysis...${NC}"
python3 scripts/kyber_security_analysis.py > results/security_analysis_results.txt
echo "   Output saved to: results/security_analysis_results.txt"

# 2. Run individual parameter tests
echo -e "\n${GREEN}2. Running individual parameter tests...${NC}"

# Test Result 5 (du=10, dv=4)
echo -e "   ${BLUE}Running Test Result 5...${NC}"
python3 scripts/Kyber.py --param-set 512 --du 10 --dv 4 > results/test_result_5.txt
python3 scripts/Kyber.py --param-set 768 --du 10 --dv 4 >> results/test_result_5.txt
python3 scripts/Kyber.py --param-set 1024 --du 11 --dv 5 >> results/test_result_5.txt

# Test Result 6 (du=11, dv=3)
echo -e "   ${BLUE}Running Test Result 6...${NC}"
python3 scripts/Kyber.py --param-set 512 --du 11 --dv 3 > results/test_result_6.txt
python3 scripts/Kyber.py --param-set 768 --du 11 --dv 3 >> results/test_result_6.txt
python3 scripts/Kyber.py --param-set 1024 --du 12 --dv 4 >> results/test_result_6.txt

# Test Result 7 (du=9, dv=5)
echo -e "   ${BLUE}Running Test Result 7...${NC}"
python3 scripts/Kyber.py --param-set 512 --du 9 --dv 5 > results/test_result_7.txt
python3 scripts/Kyber.py --param-set 768 --du 9 --dv 5 >> results/test_result_7.txt
python3 scripts/Kyber.py --param-set 1024 --du 10 --dv 6 >> results/test_result_7.txt

# 3. Run eta variation tests
echo -e "\n${GREEN}3. Running eta variation tests...${NC}"
python3 scripts/Kyber.py --param-set 512 --eta1 5 --eta2 3 > results/eta_test_results.txt
python3 scripts/Kyber.py --param-set 768 --eta1 4 --eta2 4 >> results/eta_test_results.txt
python3 scripts/Kyber.py --param-set 1024 --eta1 4 --eta2 4 >> results/eta_test_results.txt

# 4. Run all tests via test runner
echo -e "\n${GREEN}4. Running comprehensive parameter tests...${NC}"
python3 scripts/run_kyber_tests.py > results/parameter_test_results.txt

# 5. Generate visualizations
echo -e "\n${GREEN}5. Generating visualizations...${NC}"
cd scripts
python3 visualize_results.py
mv *.png ../results/plots/ 2>/dev/null
cd ..

echo -e "\n${GREEN}Analysis complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Results saved in:"
echo -e "  ${BLUE}Main Analysis:${NC} results/security_analysis_results.txt"
echo -e "  ${BLUE}Test Results:${NC} results/test_result_[5,6,7].txt"
echo -e "  ${BLUE}Parameter Tests:${NC} results/parameter_test_results.txt"
echo -e "  ${BLUE}Eta Tests:${NC} results/eta_test_results.txt"
echo -e "  ${BLUE}Plots:${NC} results/plots/"