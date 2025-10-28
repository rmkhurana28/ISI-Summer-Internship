#!/bin/bash

# Create necessary directories
mkdir -p configs results/{test1,test2,test3,test4,baseline}
mkdir -p results/{kyber1024_du11_dv5,kyber1024_du10_dv6,kyber1024_du12_dv4}

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run a test
run_test() {
    local test_name=$1
    local config_file=$2
    local description=$3
    
    echo -e "${BLUE}==== $description ====${NC}"
    cp $config_file params.h
    make clean > /dev/null 2>&1
    make speed > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        ./test_speed512 > results/$test_name/kyber512.txt
        ./test_speed768 > results/$test_name/kyber768.txt
        ./test_speed1024 > results/$test_name/kyber1024.txt
        echo -e "${GREEN}✓ $test_name completed${NC}"
    else
        echo -e "${RED}✗ $test_name failed${NC}"
    fi
}

echo "Running Kyber parameter tests..."
echo "================================"

# Test 1: (du=10, dv=4) - Baseline
run_test "test1" "configs/params_test1_du10_dv4.h" "Test 1: du=10, dv=4 (baseline)"

# Test 2: (du=11, dv=3)
run_test "test2" "configs/params_test2_du11_dv3.h" "Test 2: du=11, dv=3"

# Test 3: (du=9, dv=5)
run_test "test3" "configs/params_test3_du9_dv5.h" "Test 3: du=9, dv=5"

# Test 4: Different eta values
run_test "test4" "configs/params_test4_eta_variations.h" "Test 4: Modified eta values"

# Baseline: Standard parameters
run_test "baseline" "configs/params_baseline_standard.h" "Baseline: Standard Kyber parameters"

echo -e "\n${GREEN}All standard tests completed!${NC}"
echo "================================"
echo "To run Kyber1024 special tests, use: ./scripts/run_kyber1024_tests.sh"
echo "To run all tests including special, use: ./scripts/run_complete_tests.sh"