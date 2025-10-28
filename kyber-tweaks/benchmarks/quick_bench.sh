#!/bin/bash

# Quick Benchmark Script for Kyber
# Runs essential tests with fewer iterations for rapid testing

set -e

# Configuration
KYBER_DIR="../kyber/ref"
RESULTS_DIR="./results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
QUICK_RUN="${RESULTS_DIR}/quick_${TIMESTAMP}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Create results directory
mkdir -p "${QUICK_RUN}"

echo -e "${GREEN}=== Kyber Quick Benchmark ===${NC}"
echo "Timestamp: ${TIMESTAMP}"
echo "Results: ${QUICK_RUN}"
echo
echo "This runs a subset of tests with fewer iterations for quick validation"
echo

# Function to run quick test using existing test_speed binaries
run_quick_test() {
    local test_name=$1
    local config_file=$2
    local description=$3
    local run_full=$4  # "yes" to run all variants, "no" for just 512
    
    echo -e "${YELLOW}Testing: ${test_name}${NC}"
    echo "Config: ${config_file}"
    
    # Get absolute path
    local BENCHMARK_DIR=$(pwd)
    
    # Create test subdirectory
    mkdir -p "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}"
    
    # Save metadata
    cat > "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/metadata.txt" << EOF
Test Name: ${test_name}
Config File: ${config_file}
Description: ${description}
Timestamp: $(date)
Type: Quick Benchmark
EOF
    
    # Change to Kyber directory
    cd "${KYBER_DIR}"
    
    # Apply configuration
    if [ -f "configs/${config_file}" ]; then
        cp "configs/${config_file}" params.h
    else
        echo -e "${RED}Error: Config file not found${NC}"
        cd "${BENCHMARK_DIR}"
        return 1
    fi
    
    # Build
    echo -n "  Building... "
    make clean > /dev/null 2>&1
    
    # Instead of creating new test file, modify the Makefile temporarily
    # to use fewer iterations by defining NTESTS
    export CFLAGS="-Wall -Wextra -O3 -fomit-frame-pointer -march=native -fPIC -DNTESTS=1000"
    make speed > /dev/null 2>&1
    unset CFLAGS
    
    echo -e "${GREEN}✓${NC}"
    
    # Determine which variants to test
    if [ "$run_full" = "yes" ]; then
        variants="512 768 1024"
    else
        variants="512"  # Just test smallest variant for speed
    fi
    
    # Run tests
    for variant in $variants; do
        if [ -x "./test_speed${variant}" ]; then
            echo "  Testing Kyber${variant}..."
            # Run with timeout to prevent hanging
            timeout 30 ./test_speed${variant} > "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}.txt" 2>&1 || {
                echo -e "  ${RED}Timeout or error for Kyber${variant}${NC}"
            }
        fi
    done
    
    cd "${BENCHMARK_DIR}"
    echo -e "${GREEN}  ✓ Completed${NC}"
    echo
}

# Alternative approach: Use existing binaries but run fewer operations
run_quick_sampling() {
    local test_name=$1
    local config_file=$2
    local description=$3
    local variant=$4
    
    echo -e "${YELLOW}Quick sampling: ${test_name} (Kyber${variant})${NC}"
    
    local BENCHMARK_DIR=$(pwd)
    mkdir -p "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}"
    
    cd "${KYBER_DIR}"
    
    # Apply configuration
    if [ -f "configs/${config_file}" ]; then
        cp "configs/${config_file}" params.h
        make clean > /dev/null 2>&1
        make speed > /dev/null 2>&1
        
        if [ -x "./test_speed${variant}" ]; then
            # Run the test but kill it after getting initial results
            timeout 5 ./test_speed${variant} > "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt" 2>&1 || true
            
            # Extract just the first occurrence of each operation
            grep -m1 "poly_compress:" "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt" > "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}.txt" || true
            grep -m1 "indcpa_keypair:" "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt" >> "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}.txt" || true
            grep -m1 "indcpa_enc:" "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt" >> "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}.txt" || true
            grep -m1 "indcpa_dec:" "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt" >> "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}.txt" || true
            
            rm -f "${BENCHMARK_DIR}/${QUICK_RUN}/${test_name}/kyber${variant}_sample.txt"
        fi
    fi
    
    cd "${BENCHMARK_DIR}"
}

# Main execution
echo -e "${GREEN}Starting quick benchmark suite...${NC}"
echo

# Parse command line arguments
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --full    Run all variants (512/768/1024) instead of just 512"
    echo "  --test N  Run only specific test (1-5)"
    echo "  --help    Show this help"
    exit 0
fi

RUN_MODE="quick"  # Default: only Kyber512
SPECIFIC_TEST=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            RUN_MODE="full"
            shift
            ;;
        --test)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Determine run mode
if [ "$RUN_MODE" = "full" ]; then
    RUN_ALL="yes"
    echo "Mode: Full (all variants)"
else
    RUN_ALL="no"
    echo "Mode: Quick (Kyber512 only)"
fi
echo

# Define tests to run
run_test() {
    local test_num=$1
    
    case $test_num in
        1)
            run_quick_sampling "baseline_standard" \
                "params_baseline_standard.h" \
                "Standard Kyber parameters" \
                "512"
            ;;
        2)
            run_quick_sampling "compression_du11_dv3" \
                "params_test2_du11_dv3.h" \
                "Compression (11,3) - minimal overhead" \
                "512"
            ;;
        3)
            run_quick_sampling "compression_du9_dv5" \
                "params_test3_du9_dv5.h" \
                "Compression (9,5) - high compression" \
                "512"
            ;;
        4)
            run_quick_sampling "eta_variations" \
                "params_test4_eta_variations.h" \
                "Modified eta values" \
                "512"
            ;;
    esac
}

# Run tests
if [ -n "$SPECIFIC_TEST" ]; then
    echo "Running only test $SPECIFIC_TEST"
    run_test "$SPECIFIC_TEST"
else
    echo "Running quick sampling tests..."
    for i in 1 2 3 4; do
        run_test "$i"
    done
fi

# Quick analysis
echo -e "${GREEN}=== Quick Benchmark Complete ===${NC}"
echo "Results saved in: ${QUICK_RUN}"
echo

# Generate quick summary
cat > "${QUICK_RUN}/quick_summary.txt" << 'EOF'
QUICK BENCHMARK SUMMARY
======================

This quick benchmark provides rapid feedback by:
1. Running existing test binaries with timeout
2. Capturing first results only (not full 10k iterations)
3. Testing only Kyber512 by default

For accurate results, run full benchmark: ./run_cycle_counts.sh
EOF

echo "Timestamp: ${TIMESTAMP}" >> "${QUICK_RUN}/quick_summary.txt"
echo "Tests executed:" >> "${QUICK_RUN}/quick_summary.txt"

for test_dir in "${QUICK_RUN}"/*/; do
    if [ -d "$test_dir" ]; then
        test_name=$(basename "$test_dir")
        echo "- ${test_name}" >> "${QUICK_RUN}/quick_summary.txt"
        
        # Show first result from each test
        if [ -f "${test_dir}/kyber512.txt" ]; then
            echo "  Sample results:" >> "${QUICK_RUN}/quick_summary.txt"
            head -4 "${test_dir}/kyber512.txt" | sed 's/^/    /' >> "${QUICK_RUN}/quick_summary.txt"
        fi
    fi
done

# Display summary
echo
cat "${QUICK_RUN}/quick_summary.txt"

echo
echo -e "${GREEN}Quick benchmark complete!${NC}"
echo
echo "This was a rapid test. For full results:"
echo "1. Run complete benchmark: ./run_cycle_counts.sh"
echo "2. Run specific test: $0 --test N (where N is 1-4)"
echo