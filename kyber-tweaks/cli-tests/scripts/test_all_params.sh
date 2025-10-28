#!/bin/bash

# Test all parameter configurations
# This script demonstrates encryption/decryption with each parameter set

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_TEST_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Kyber source directory
KYBER_DIR="$CLI_TEST_DIR/../kyber/ref"
RESULTS_DIR="$CLI_TEST_DIR/test_results"

# Create results directory
mkdir -p "$RESULTS_DIR"

echo -e "${GREEN}=== Kyber Parameter Configuration Tests ===${NC}\n"

# Function to test a configuration
test_config() {
    local config_name=$1
    local config_file=$2
    local description=$3
    
    echo -e "${YELLOW}Testing: $config_name${NC}"
    echo "Description: $description"
    
    # Apply configuration
    if [ ! -f "$KYBER_DIR/configs/$config_file" ]; then
        echo -e "${RED}Error: Config file not found: $KYBER_DIR/configs/$config_file${NC}"
        return 1
    fi
    
    cp "$KYBER_DIR/configs/$config_file" "$KYBER_DIR/params.h"
    
    # Go to CLI test directory and rebuild
    cd "$CLI_TEST_DIR"
    echo -n "Building... "
    make clean > /dev/null 2>&1
    make all > /dev/null 2>&1
    echo -e "${GREEN}✓${NC}"
    
    # Create test directory
    mkdir -p "$RESULTS_DIR/$config_name"
    cd "$RESULTS_DIR/$config_name"
    
    # Generate keys
    echo -n "Generating keys... "
    "$CLI_TEST_DIR/kyber_keygen" -o test -v > keygen.log 2>&1
    echo -e "${GREEN}✓${NC}"
    
    # Encrypt
    echo -n "Encrypting... "
    "$CLI_TEST_DIR/kyber_encrypt" -k test.pub -o ct.bin -s ss_enc.bin -v > encrypt.log 2>&1
    echo -e "${GREEN}✓${NC}"
    
    # Decrypt
    echo -n "Decrypting... "
    "$CLI_TEST_DIR/kyber_decrypt" -s test.sec -c ct.bin -o ss_dec.bin -v > decrypt.log 2>&1
    echo -e "${GREEN}✓${NC}"
    
    # Verify
    echo -n "Verifying... "
    if cmp ss_enc.bin ss_dec.bin > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Shared secrets match!${NC}"
        echo "SUCCESS" > result.txt
    else
        echo -e "${RED}✗ Shared secrets don't match!${NC}"
        echo "FAILED" > result.txt
    fi
    
    # Save sizes
    echo "Sizes:" > sizes.txt
    echo "Public key: $(ls -l test.pub | awk '{print $5}') bytes" >> sizes.txt
    echo "Secret key: $(ls -l test.sec | awk '{print $5}') bytes" >> sizes.txt
    echo "Ciphertext: $(ls -l ct.bin | awk '{print $5}') bytes" >> sizes.txt
    
    # Run demo in quick mode
    "$CLI_TEST_DIR/kyber_demo" -q > demo.log 2>&1
    
    echo
}

# Test all configurations
echo "Testing standard Kyber configurations..."
test_config "baseline_standard" \
    "params_baseline_standard.h" \
    "Standard NIST Round 3 parameters"

test_config "test1_du10_dv4" \
    "params_test1_du10_dv4.h" \
    "Standard compression (du=10, dv=4)"

test_config "test2_du11_dv3" \
    "params_test2_du11_dv3.h" \
    "Reduced compression (du=11, dv=3) - smaller ciphertext"

test_config "test3_du9_dv5" \
    "params_test3_du9_dv5.h" \
    "High compression (du=9, dv=5) - smallest ciphertext"

test_config "test4_eta_variations" \
    "params_test4_eta_variations.h" \
    "Modified noise parameters (increased eta)"

# Summary
echo -e "${GREEN}=== Test Summary ===${NC}"
echo
for dir in "$RESULTS_DIR"/*/; do
    if [ -d "$dir" ]; then
        config=$(basename "$dir")
        result=$(cat "$dir/result.txt" 2>/dev/null || echo "N/A")
        if [ "$result" == "SUCCESS" ]; then
            echo -e "$config: ${GREEN}PASSED${NC}"
        else
            echo -e "$config: ${RED}FAILED${NC}"
        fi
        
        # Show sizes
        if [ -f "$dir/sizes.txt" ]; then
            cat "$dir/sizes.txt" | sed 's/^/  /'
        fi
        echo
    fi
done

echo -e "${GREEN}All tests complete!${NC}"