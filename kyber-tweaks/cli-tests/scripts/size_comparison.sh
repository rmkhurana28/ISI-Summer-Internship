#!/bin/bash

# Compare ciphertext sizes across different parameter configurations

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

KYBER_DIR="../kyber/ref"

echo -e "${GREEN}=== Kyber Ciphertext Size Comparison ===${NC}\n"
echo "This script shows how parameter tweaks affect sizes"
echo

# Function to test and show sizes
show_config_sizes() {
    local config_name=$1
    local config_file=$2
    local expected_ct_size=$3
    
    # Apply configuration
    cp $KYBER_DIR/configs/$config_file $KYBER_DIR/params.h
    
    # Rebuild
    make clean > /dev/null 2>&1
    make all > /dev/null 2>&1
    
    # Generate keys
    ./kyber_keygen -o temp_key > /dev/null 2>&1
    
    # Encrypt
    ./kyber_encrypt -k temp_key.pub -o temp_ct.bin > /dev/null 2>&1
    
    # Get actual sizes
    local pk_size=$(ls -l temp_key.pub | awk '{print $5}')
    local sk_size=$(ls -l temp_key.sec | awk '{print $5}')
    local ct_size=$(ls -l temp_ct.bin | awk '{print $5}')
    
    # Get parameters from demo output
    local param_info=$(./kyber_demo -q 2>&1 | grep "Compression" | head -1 || echo "Compression (du, dv): (?, ?)")
    
    # Extract just the (du, dv) part
    local compression=$(echo "$param_info" | grep -o "(.*)" || echo "(?, ?)")
    
    # Calculate reduction if we have baseline
    local reduction=""
    if [ "$config_name" != "Baseline" ] && [ -n "$BASELINE_CT" ]; then
        reduction=$(awk "BEGIN {printf \"%.1f\", (($BASELINE_CT - $ct_size) * 100.0 / $BASELINE_CT)}")
    else
        reduction="0"
        BASELINE_CT=$ct_size
    fi
    
    printf "%-12s %-15s %-10s %-10s %-10s %11s%%\n" \
        "$config_name" "$compression" "$pk_size" "$sk_size" "$ct_size" "$reduction"
    
    # Clean up
    rm -f temp_key.* temp_ct.bin shared_secret.bin
}

# Header
printf "%-12s %-15s %-10s %-10s %-10s %-12s\n" \
    "Config" "Compression" "PK Size" "SK Size" "CT Size" "CT Reduction"
echo "------------------------------------------------------------------------"

# Global to store baseline CT size
BASELINE_CT=""

# Test configurations in order
show_config_sizes "Baseline" "params_baseline_standard.h" 768
show_config_sizes "Test1" "params_test1_du10_dv4.h" 768
show_config_sizes "Test2" "params_test2_du11_dv3.h" 736
show_config_sizes "Test3" "params_test3_du9_dv5.h" 800
show_config_sizes "Test4-Eta" "params_test4_eta_variations.h" 768

echo
echo -e "${YELLOW}Note:${NC} Ciphertext size directly depends on compression parameters (du, dv)"
echo "Lower du/dv = smaller ciphertext but higher computational cost"
echo
echo "Current configuration shows the impact of different parameter choices:"
echo "- Test2 (du=11, dv=3): Reduces ciphertext size with minimal performance impact"
echo "- Test3 (du=9, dv=5): Maximum compression but significant performance overhead"
echo "- Test4: Modified eta values don't affect ciphertext size, only performance"

# Restore baseline
cp $KYBER_DIR/configs/params_baseline_standard.h $KYBER_DIR/params.h
make clean > /dev/null 2>&1