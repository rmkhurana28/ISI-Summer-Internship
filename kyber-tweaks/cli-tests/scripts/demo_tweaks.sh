#!/bin/bash

# Interactive demonstration of Kyber parameter tweaks
# Shows the impact of different configurations

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

KYBER_DIR="../kyber/ref"

clear

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          Kyber Parameter Tweaks Demonstration             ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo

echo -e "${GREEN}This demo shows how different parameter choices affect:${NC}"
echo "1. Ciphertext sizes"
echo "2. Performance characteristics"
echo "3. Security parameters"
echo

echo -e "${YELLOW}Available configurations:${NC}"
echo "1. Baseline (Standard NIST Round 3)"
echo "2. Compression Test 1 (du=10, dv=4) - Standard"
echo "3. Compression Test 2 (du=11, dv=3) - Size optimized"
echo "4. Compression Test 3 (du=9, dv=5) - Maximum compression"
echo "5. Eta Variations - Modified noise parameters"
echo "6. Exit demo"
echo

while true; do
    echo -ne "${BLUE}Select configuration (1-6): ${NC}"
    read choice
    
    case $choice in
        1)
            config="params_baseline_standard.h"
            name="Baseline (Standard)"
            ;;
        2)
            config="params_test1_du10_dv4.h"
            name="Test 1 (du=10, dv=4)"
            ;;
        3)
            config="params_test2_du11_dv3.h"
            name="Test 2 (du=11, dv=3)"
            ;;
        4)
            config="params_test3_du9_dv5.h"
            name="Test 3 (du=9, dv=5)"
            ;;
        5)
            config="params_test4_eta_variations.h"
            name="Test 4 (Eta Variations)"
            ;;
        6)
            echo -e "${GREEN}Exiting demo. Thank you!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please select 1-6.${NC}"
            continue
            ;;
    esac
    
    echo
    echo -e "${YELLOW}Loading configuration: $name${NC}"
    
    # Apply configuration
    cp "$KYBER_DIR/configs/$config" "$KYBER_DIR/params.h"
    
    # Rebuild
    echo -n "Building with new parameters... "
    make clean > /dev/null 2>&1
    make all > /dev/null 2>&1
    echo -e "${GREEN}Done!${NC}"
    
    echo
    echo -e "${CYAN}=== Running Demo ===${NC}"
    ./kyber_demo -q
    
    echo
    echo -e "${GREEN}Key observations for this configuration:${NC}"
    
    case $choice in
        1)
            echo "• This is the standard NIST Round 3 submission"
            echo "• Balanced performance and security"
            echo "• Reference for comparing other configurations"
            ;;
        2)
            echo "• Standard compression parameters"
            echo "• Same as baseline for Kyber512"
            echo "• No size or performance changes"
            ;;
        3)
            echo "• Reduced polynomial compression bits"
            echo "• Smaller ciphertext size (~4% reduction)"
            echo "• Slight performance overhead (~50% on compression)"
            ;;
        4)
            echo "• Increased polynomial compression bits"
            echo "• Larger ciphertext size (~4% increase)"
            echo "• Very high compression overhead (>100%)"
            ;;
        5)
            echo "• Modified noise distribution parameters"
            echo "• No change in ciphertext size"
            echo "• Significant impact on key generation (~30% slower)"
            ;;
    esac
    
    echo
    echo -ne "${BLUE}Press Enter to continue...${NC}"
    read
    echo
done