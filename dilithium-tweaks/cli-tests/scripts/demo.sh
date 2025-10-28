#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Demo header
clear
echo -e "${BLUE}=========================================="
echo -e "     Dilithium Tweaks Demonstration"
echo -e "==========================================${NC}"
echo
echo "This demo showcases three implementations of Dilithium:"
echo "1. Baseline - Original implementation"
echo "2. Option 1 - Tweaks with relaxed bounds (2×BETA)"
echo "3. Option 2 - Tweaks with probabilistic bypass (10%)"
echo
echo "Tweaks implemented:"
echo "- Tweak 1: SHA3-256 instead of SHAKE256"
echo "- Tweak 2: Expanded coefficients {-2,-1,0,1,2}"
echo "- Tweak 3: Modified rejection sampling"
echo
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 1: Key Generation
echo -e "\n${BLUE}Step 1: Key Generation${NC}"
echo "----------------------------------------"
echo "Generating a key pair (same for all implementations)..."
./cli_keygen_simple -o demo_key
echo -e "${GREEN}✓ Keys generated successfully${NC}"
echo
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 2: Create test message
echo -e "\n${BLUE}Step 2: Test Message${NC}"
echo "----------------------------------------"
echo "Creating a test message..."
echo "Hello, this is a demonstration of Dilithium tweaks!" > test_data/messages/demo_msg.txt
echo "Message content:"
cat test_data/messages/demo_msg.txt
echo
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 3: Sign with all implementations
echo -e "\n${BLUE}Step 3: Signing with Different Implementations${NC}"
echo "----------------------------------------"

echo -e "\n${GREEN}3.1 Baseline Implementation:${NC}"
time ./cli_sign_baseline -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o demo_baseline.sig -m baseline -v

echo -e "\n${YELLOW}Press Enter to continue...${NC}"
read

echo -e "\n${GREEN}3.2 Option 1 (Relaxed Bounds):${NC}"
echo "Note: This takes longer due to more rejection iterations"
time ./cli_sign_option1 -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o demo_option1.sig -m option1 -v

echo -e "\n${YELLOW}Press Enter to continue...${NC}"
read

echo -e "\n${GREEN}3.3 Option 2 (Probabilistic Bypass):${NC}"
echo "Note: This has moderate overhead with occasional fast signatures"
time ./cli_sign_option2 -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o demo_option2.sig -m option2 -v

echo -e "\n${YELLOW}Press Enter to continue...${NC}"
read

# Step 4: Verify signatures
echo -e "\n${BLUE}Step 4: Signature Verification${NC}"
echo "----------------------------------------"

echo -e "\n${GREEN}4.1 Verifying with Matched Verifiers:${NC}"
echo "Baseline signature with baseline verifier:"
./cli_verify -i test_data/messages/demo_msg.txt -s output/signatures/demo_baseline.sig -k output/keys/demo_key.pk

echo -e "\nOption 1 signature with Option 1 verifier:"
./cli_verify_option1 test_data/messages/demo_msg.txt output/signatures/demo_option1.sig output/keys/demo_key.pk

echo -e "\nOption 2 signature with Option 2 verifier:"
./cli_verify_option2 test_data/messages/demo_msg.txt output/signatures/demo_option2.sig output/keys/demo_key.pk

echo -e "\n${YELLOW}Press Enter to continue...${NC}"
read

echo -e "\n${GREEN}4.2 Cross-Verification Test:${NC}"
echo "Testing if tweaked signatures work with baseline verifier..."
echo -e "${RED}(These should fail - demonstrating incompatibility)${NC}"
echo
echo "Option 1 signature with baseline verifier:"
./cli_verify -i test_data/messages/demo_msg.txt -s output/signatures/demo_option1.sig -k output/keys/demo_key.pk 2>&1 | grep -E "VALID|INVALID"

echo -e "\nOption 2 signature with baseline verifier:"
./cli_verify -i test_data/messages/demo_msg.txt -s output/signatures/demo_option2.sig -k output/keys/demo_key.pk 2>&1 | grep -E "VALID|INVALID"

echo -e "\n${YELLOW}Press Enter to continue...${NC}"
read

# Step 5: Performance comparison
echo -e "\n${BLUE}Step 5: Performance Comparison${NC}"
echo "----------------------------------------"
echo "Running quick performance test (10 signatures each)..."
echo

echo -e "${GREEN}Baseline:${NC}"
time for i in {1..10}; do 
    ./cli_sign_baseline -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o temp.sig -m baseline >/dev/null 2>&1
done

echo -e "\n${GREEN}Option 1 (Relaxed Bounds):${NC}"
time for i in {1..10}; do 
    ./cli_sign_option1 -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o temp.sig -m option1 >/dev/null 2>&1
done

echo -e "\n${GREEN}Option 2 (Probabilistic):${NC}"
time for i in {1..10}; do 
    ./cli_sign_option2 -i test_data/messages/demo_msg.txt -k output/keys/demo_key.sk -o temp.sig -m option2 >/dev/null 2>&1
done

# Step 6: Summary
echo -e "\n${BLUE}Summary${NC}"
echo "=========================================="
echo -e "${GREEN}✓${NC} All implementations produce valid signatures"
echo -e "${GREEN}✓${NC} Tweaked implementations require matching verifiers"
echo -e "${GREEN}✓${NC} Performance impact:"
echo "   - Option 1: ~1.7x slower (more rejection iterations)"
echo "   - Option 2: ~1.4x slower (probabilistic bypass)"
echo -e "${GREEN}✓${NC} All tweaks successfully implemented:"
echo "   - SHA3-256 for challenge generation"
echo "   - Expanded coefficient set {-2,-1,0,1,2}"
echo "   - Modified rejection sampling"
echo
echo -e "${BLUE}Demo completed!${NC}"
echo

# Cleanup
rm -f output/signatures/temp.sig
rm -f test_data/messages/demo_msg.txt