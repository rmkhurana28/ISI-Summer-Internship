#!/bin/bash

# Kyber Cycle Count Benchmarking Script
# Collects cycle counts for all parameter variations

set -e  # Exit on error

# Configuration
KYBER_DIR="../kyber/ref"
RESULTS_DIR="./results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CURRENT_RUN="${RESULTS_DIR}/run_${TIMESTAMP}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create results directory for this run
mkdir -p "${CURRENT_RUN}"

echo -e "${GREEN}=== Kyber Cycle Count Benchmarking ===${NC}"
echo "Timestamp: ${TIMESTAMP}"
echo "Results directory: ${CURRENT_RUN}"
echo

# Function to run cycle count test
run_cycle_test() {
    local test_name=$1
    local config_file=$2
    local description=$3
    
    echo -e "${YELLOW}Running: ${test_name}${NC}"
    echo "Config: ${config_file}"
    echo "Description: ${description}"
    
    # Get absolute path of current directory
    local BENCHMARK_DIR=$(pwd)
    
    # Create test subdirectory
    mkdir -p "${BENCHMARK_DIR}/${CURRENT_RUN}/${test_name}"
    
    # Save test metadata
    cat > "${BENCHMARK_DIR}/${CURRENT_RUN}/${test_name}/metadata.txt" << EOF
Test Name: ${test_name}
Config File: ${config_file}
Description: ${description}
Timestamp: $(date)
EOF
    
    # Change to Kyber directory
    cd "${KYBER_DIR}"
    
    # Apply configuration
    if [ -f "configs/${config_file}" ]; then
        cp "configs/${config_file}" params.h
    else
        echo -e "${RED}Error: Config file not found: configs/${config_file}${NC}"
        cd "${BENCHMARK_DIR}"
        return 1
    fi
    
    # Clean and build
    echo "  Building..."
    make clean > /dev/null 2>&1
    make speed > "${BENCHMARK_DIR}/${CURRENT_RUN}/${test_name}/build_log.txt" 2>&1
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}  Build failed! Check ${CURRENT_RUN}/${test_name}/build_log.txt${NC}"
        cd "${BENCHMARK_DIR}"
        return 1
    fi
    
    # Run tests for each variant
    for variant in 512 768 1024; do
        if [ -x "./test_speed${variant}" ]; then
            echo "  Testing Kyber${variant}..."
            ./test_speed${variant} > "${BENCHMARK_DIR}/${CURRENT_RUN}/${test_name}/kyber${variant}.txt" 2>&1
        else
            echo -e "${RED}  test_speed${variant} not found!${NC}"
        fi
    done
    
    cd "${BENCHMARK_DIR}"
    echo -e "${GREEN}  ✓ Completed${NC}"
    echo
}

# Main benchmark execution
echo -e "${GREEN}Starting benchmark suite...${NC}"
echo

# 1. Baseline configuration
run_cycle_test "baseline_standard" \
    "params_baseline_standard.h" \
    "Standard Kyber parameters (reference)"

# 2. Compression parameter variations
run_cycle_test "test1_compression_du10_dv4" \
    "params_test1_du10_dv4.h" \
    "Compression parameters: du=10, dv=4"

run_cycle_test "test2_compression_du11_dv3" \
    "params_test2_du11_dv3.h" \
    "Compression parameters: du=11, dv=3"

run_cycle_test "test3_compression_du9_dv5" \
    "params_test3_du9_dv5.h" \
    "Compression parameters: du=9, dv=5"

# 3. Eta variations
run_cycle_test "test4_eta_variations" \
    "params_test4_eta_variations.h" \
    "Modified eta values for noise distribution"

# 4. Special Kyber1024 configurations
run_cycle_test "kyber1024_special_du11_dv5" \
    "params_kyber1024_du11_dv5.h" \
    "Kyber1024 with du=11, dv=5"

run_cycle_test "kyber1024_special_du10_dv6" \
    "params_kyber1024_du10_dv6.h" \
    "Kyber1024 with du=10, dv=6"

run_cycle_test "kyber1024_special_du12_dv4" \
    "params_kyber1024_du12_dv4.h" \
    "Kyber1024 with du=12, dv=4"

echo -e "${GREEN}=== Benchmarking Complete ===${NC}"
echo "Results saved in: ${CURRENT_RUN}"
echo

# Create summary
echo "Generating quick summary..."
echo "=== BENCHMARK RUN SUMMARY ===" > "${CURRENT_RUN}/summary.txt"
echo "Timestamp: ${TIMESTAMP}" >> "${CURRENT_RUN}/summary.txt"
echo "Tests executed:" >> "${CURRENT_RUN}/summary.txt"
echo >> "${CURRENT_RUN}/summary.txt"

for test_dir in "${CURRENT_RUN}"/*/; do
    if [ -d "$test_dir" ]; then
        test_name=$(basename "$test_dir")
        echo "- ${test_name}" >> "${CURRENT_RUN}/summary.txt"
        if [ -f "${test_dir}/metadata.txt" ]; then
            grep "Description:" "${test_dir}/metadata.txt" >> "${CURRENT_RUN}/summary.txt"
        fi
        echo >> "${CURRENT_RUN}/summary.txt"
    fi
done

echo -e "${GREEN}Summary saved in: ${CURRENT_RUN}/summary.txt${NC}"