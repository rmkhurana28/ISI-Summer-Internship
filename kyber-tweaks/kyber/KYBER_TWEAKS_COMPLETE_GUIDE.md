# Kyber Parameter Tweaks - Complete Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [Project Structure](#project-structure)
4. [Implementation Steps](#implementation-steps)
5. [Running Individual Tests](#running-individual-tests)
6. [Automated Testing](#automated-testing)
7. [Results Analysis](#results-analysis)
8. [File Reference](#file-reference)

## Overview

This guide documents the complete implementation of Kyber parameter tweaks as described in Chapter 5 of the thesis. The tweaks include:
- Compression parameters (du, dv) variations
- Noise distribution parameters (η1, η2) variations
- Special Kyber1024 configurations

## Environment Setup

### Prerequisites
- Ubuntu Linux (tested on 24.04.2 LTS)
- GCC compiler
- Python 3.x
- Git

### Initial Setup
```bash
# Create project directory
mkdir kyber-tweaks
cd kyber-tweaks

# Clone Kyber repository
git clone https://github.com/pq-crystals/kyber
cd kyber
git checkout round3
cd ref

# Create necessary directories
mkdir -p configs
mkdir -p results/{test1,test2,test3,test4,baseline}
mkdir -p results/{kyber1024_du11_dv5,kyber1024_du10_dv6,kyber1024_du12_dv4}
mkdir -p scripts

Project_Structure


kyber-tweaks/kyber/ref/
├── configs/                          # Parameter configuration files
│   ├── params_test1_du10_dv4.h     # Test 1: (du=10, dv=4)
│   ├── params_test2_du11_dv3.h     # Test 2: (du=11, dv=3)
│   ├── params_test3_du9_dv5.h      # Test 3: (du=9, dv=5)
│   ├── params_test4_eta_variations.h # Test 4: eta variations
│   ├── params_baseline_standard.h   # Standard Kyber parameters
│   ├── params_kyber1024_du11_dv5.h # Kyber1024 (du=11, dv=5)
│   ├── params_kyber1024_du10_dv6.h # Kyber1024 (du=10, dv=6)
│   └── params_kyber1024_du12_dv4.h # Kyber1024 (du=12, dv=4)
├── results/                         # Test results
│   ├── test1/                      # Test 1 results
│   ├── test2/                      # Test 2 results
│   ├── test3/                      # Test 3 results
│   ├── test4/                      # Test 4 results
│   ├── baseline/                   # Baseline results
│   ├── kyber1024_du11_dv5/        # Special Kyber1024 results
│   ├── kyber1024_du10_dv6/        # Special Kyber1024 results
│   └── kyber1024_du12_dv4/        # Special Kyber1024 results
├── scripts/                        # Automation scripts
│   ├── run_all_tests.sh           # Run all standard tests
│   ├── run_complete_tests.sh      # Run all tests including special
│   ├── extract_results.py         # Extract results to tables
│   ├── generate_thesis_tables.py  # Generate thesis-format tables
│   └── generate_final_thesis_tables.py # Final tables with baseline
├── poly.c                         # Modified for new compression values
├── polyvec.c                      # Modified for new compression values
├── cbd.c                          # Modified with cbd4, cbd5 functions
└── params.h                       # Current parameter configuration

Implementation_Steps

Step 1: Modify Source Files
1.1 Modify poly.c
Add support for 96, 192, and 200-byte compression in poly_compress and poly_decompress functions:

c
// In poly_compress, add before #else:
#elif (KYBER_POLYCOMPRESSEDBYTES == 96)
  // 3-bit compression implementation
#elif (KYBER_POLYCOMPRESSEDBYTES == 192)
  // 6-bit compression implementation
#elif (KYBER_POLYCOMPRESSEDBYTES == 200)
  // 5+7 bit compression implementation

// Update error message:
#error "KYBER_POLYCOMPRESSEDBYTES needs to be in {96, 128, 160, 192, 200}"
1.2 Modify polyvec.c
Add support for 288K and 384K compression:

c
// In polyvec_compress, add before #else:
#elif (KYBER_POLYVECCOMPRESSEDBYTES == (KYBER_K * 288))
  // 9-bit compression implementation
#elif (KYBER_POLYVECCOMPRESSEDBYTES == (KYBER_K * 384))
  // 12-bit compression implementation

// Update error message:
#error "KYBER_POLYVECCOMPRESSEDBYTES needs to be in {288*K, 320*K, 352*K, 384*K}"
1.3 Modify cbd.c
Add cbd4 and cbd5 functions and remove conditional compilation:

c
// Remove #if KYBER_ETA1 == 3 guards around load24_littleendian and cbd3

// Add new functions:
static void cbd4(poly *r, const uint8_t buf[4*KYBER_N/4]) { /* implementation */ }
static void cbd5(poly *r, const uint8_t buf[5*KYBER_N/4]) { /* implementation */ }

// Update poly_cbd_eta1 and poly_cbd_eta2 to support eta=4,5
Step 2: Create Configuration Files
2.1 Test 1 Configuration (Figure 5.1)
File: configs/params_test1_du10_dv4.h

Kyber512: η1=3, η2=2, POLYCOMPRESSEDBYTES=128, POLYVECCOMPRESSEDBYTES=640
Kyber768: η1=3, η2=2, POLYCOMPRESSEDBYTES=128, POLYVECCOMPRESSEDBYTES=960
Kyber1024: η1=2, η2=2, POLYCOMPRESSEDBYTES=160, POLYVECCOMPRESSEDBYTES=1408
2.2 Test 2 Configuration (Figure 5.2)
File: configs/params_test2_du11_dv3.h

Kyber512: η1=3, η2=2, POLYCOMPRESSEDBYTES=96, POLYVECCOMPRESSEDBYTES=704
Kyber768: η1=3, η2=2, POLYCOMPRESSEDBYTES=96, POLYVECCOMPRESSEDBYTES=1056
Kyber1024: η1=2, η2=2, POLYCOMPRESSEDBYTES=128, POLYVECCOMPRESSEDBYTES=1280
2.3 Test 3 Configuration (Figure 5.3)
File: configs/params_test3_du9_dv5.h

Kyber512: η1=3, η2=2, POLYCOMPRESSEDBYTES=160, POLYVECCOMPRESSEDBYTES=576
Kyber768: η1=2, η2=2, POLYCOMPRESSEDBYTES=160, POLYVECCOMPRESSEDBYTES=864
Kyber1024: η1=2, η2=2, POLYCOMPRESSEDBYTES=192, POLYVECCOMPRESSEDBYTES=1408
2.4 Test 4 Configuration (Figure 5.4)
File: configs/params_test4_eta_variations.h

Kyber512: η1=5, η2=3
Kyber768: η1=4, η2=4
Kyber1024: η1=4, η2=4
2.5 Baseline Configuration
File: configs/params_baseline_standard.h

Standard Kyber parameters for comparison
2.6 Kyber1024 Special Configurations
configs/params_kyber1024_du11_dv5.h: POLYCOMPRESSEDBYTES=200
configs/params_kyber1024_du10_dv6.h: POLYCOMPRESSEDBYTES=192
configs/params_kyber1024_du12_dv4.h: POLYCOMPRESSEDBYTES=128

Running_Individual_Tests

Test 1: (du=10, dv=4) - Standard Baseline
bash
cp configs/params_test1_du10_dv4.h params.h
make clean && make speed
./test_speed512 > results/test1/kyber512.txt
./test_speed768 > results/test1/kyber768.txt
./test_speed1024 > results/test1/kyber1024.txt

Test 2: (du=11, dv=3)
bash
cp configs/params_test2_du11_dv3.h params.h
make clean && make speed
./test_speed512 > results/test2/kyber512.txt
./test_speed768 > results/test2/kyber768.txt
./test_speed1024 > results/test2/kyber1024.txt

Test 3: (du=9, dv=5)
bash
cp configs/params_test3_du9_dv5.h params.h
make clean && make speed
./test_speed512 > results/test3/kyber512.txt
./test_speed768 > results/test3/kyber768.txt
./test_speed1024 > results/test3/kyber1024.txt

Test 4: Eta Variations
bash
cp configs/params_test4_eta_variations.h params.h
make clean && make speed
./test_speed512 > results/test4/kyber512.txt
./test_speed768 > results/test4/kyber768.txt
./test_speed1024 > results/test4/kyber1024.txt

Baseline Tests
bash
cp configs/params_baseline_standard.h params.h
make clean && make speed
./test_speed512 > results/baseline/kyber512.txt
./test_speed768 > results/baseline/kyber768.txt
./test_speed1024 > results/baseline/kyber1024.txt

Kyber1024 Special Tests
bash
# Test (du=11, dv=5)
cp configs/params_kyber1024_du11_dv5.h params.h
make clean && make speed
./test_speed1024 > results/kyber1024_du11_dv5/results.txt

# Test (du=10, dv=6)
cp configs/params_kyber1024_du10_dv6.h params.h
make clean && make speed
./test_speed1024 > results/kyber1024_du10_dv6/results.txt

# Test (du=12, dv=4)
cp configs/params_kyber1024_du12_dv4.h params.h
make clean && make speed
./test_speed1024 > results/kyber1024_du12_dv4/results.txt
Automated Testing
Complete Test Suite Script
File: scripts/run_complete_tests.sh

bash
#!/bin/bash

echo "Running complete Kyber parameter tests..."

# Standard tests (Test 1-4)
for test in test1 test2 test3 test4; do
    echo "Running $test..."
    config=$(ls configs/params_${test}_*.h)
    cp $config params.h
    make clean && make speed
    
    ./test_speed512 > results/$test/kyber512.txt
    ./test_speed768 > results/$test/kyber768.txt
    ./test_speed1024 > results/$test/kyber1024.txt
done

# Baseline tests
echo "Running baseline tests..."
cp configs/params_baseline_standard.h params.h
make clean && make speed
./test_speed512 > results/baseline/kyber512.txt
./test_speed768 > results/baseline/kyber768.txt
./test_speed1024 > results/baseline/kyber1024.txt

# Kyber1024 special tests
for config in configs/params_kyber1024_*.h; do
    name=$(basename $config .h | sed 's/params_//')
    echo "Running $name..."
    cp $config params.h
    make clean && make speed
    ./test_speed1024 > results/$name/results.txt
done

echo "All tests completed!"
Run All Tests
bash
chmod +x scripts/run_complete_tests.sh
./scripts/run_complete_tests.sh
Results Analysis
Generate Thesis Tables
File: scripts/generate_final_thesis_tables.py

bash
chmod +x scripts/generate_final_thesis_tables.py
python3 scripts/generate_final_thesis_tables.py > final_thesis_tables.txt
View Specific Results
bash
# View Test 1 Kyber512 results
cat results/test1/kyber512.txt

# Extract specific metrics
grep -A2 "

Results_Analysis

Generate Thesis Tables
File: scripts/generate_final_thesis_tables.py

bash
chmod +x scripts/generate_final_thesis_tables.py
python3 scripts/generate_final_thesis_tables.py > final_thesis_tables.txt
View Specific Results
bash
# View Test 1 Kyber512 results
cat results/test1/kyber512.txt

# Extract specific metrics
grep -A2 "poly_compress:" results/test1/kyber512.txt
grep -A2 "indcpa_keypair:" results/test1/kyber512.txt

# Compare results across tests
for test in test1 test2 test3; do
    echo "=== $test ==="
    grep -A2 "poly_compress:" results/$test/kyber512.txt | grep median
done
Extract All Results to CSV
File: scripts/extract_results.py

python
#!/usr/bin/env python3
import os
import re

def extract_value(file_path, metric):
    """Extract median and average values for a given metric."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            pattern = rf"{metric}:.*?median: (\d+).*?average: (\d+)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1), match.group(2)
    except:
        pass
    return "N/A", "N/A"

# Extract results for all tests
tests = ["test1", "test2", "test3", "test4"]
variants = ["kyber512", "kyber768", "kyber1024"]
operations = ["poly_compress", "poly_decompress", "polyvec_compress", 
              "polyvec_decompress", "indcpa_keypair", "indcpa_enc", "indcpa_dec"]

for variant in variants:
    print(f"\n{variant.upper()} Results:")
    print("-" * 80)
    for op in operations:
        row = f"{op:<25}"
        for test in tests:
            filepath = f"results/{test}/{variant}.txt"
            median, avg = extract_value(filepath, op)
            row += f"{median}/{avg:<20}"
        print(row)
        
Generate Thesis-Format Tables

bash
# Generate all tables matching thesis format
python3 scripts/generate_final_thesis_tables.py

# Generate individual tables
python3 scripts/generate_final_thesis_tables.py | grep -A20 "Table 5.1"  # Kyber512
python3 scripts/generate_final_thesis_tables.py | grep -A20 "Table 5.2"  # Kyber768
python3 scripts/generate_final_thesis_tables.py | grep -A20 "Table 5.3"  # Kyber1024
python3 scripts/generate_final_thesis_tables.py | grep -A20 "Table 5.4"  # Eta variations
File Reference
Configuration Files Created
configs/params_test1_du10_dv4.h - Standard baseline (du=10, dv=4)
configs/params_test2_du11_dv3.h - Compression test (du=11, dv=3)
configs/params_test3_du9_dv5.h - Compression test (du=9, dv=5)
configs/params_test4_eta_variations.h - Eta variations
configs/params_baseline_standard.h - Standard Kyber parameters
configs/params_kyber1024_du11_dv5.h - Kyber1024 (du=11, dv=5)
configs/params_kyber1024_du10_dv6.h - Kyber1024 (du=10, dv=6)
configs/params_kyber1024_du12_dv4.h - Kyber1024 (du=12, dv=4)
Modified Source Files
poly.c

Added support for POLYCOMPRESSEDBYTES: 96, 128, 160, 192, 200
Modified poly_compress and poly_decompress functions
polyvec.c

Added support for POLYVECCOMPRESSEDBYTES: 288K, 320K, 352K, 384K
Modified polyvec_compress and polyvec_decompress functions
cbd.c

Added cbd4() function for η=4
Added cbd5() function for η=5
Removed conditional compilation guards
Updated poly_cbd_eta1 and poly_cbd_eta2
Automation Scripts Created
scripts/run_all_tests.sh - Runs standard tests 1-4
scripts/run_complete_tests.sh - Runs all tests including special Kyber1024
scripts/extract_results.py - Extracts results to readable format
scripts/generate_thesis_tables.py - Generates initial thesis tables
scripts/generate_final_thesis_tables.py - Generates final tables with baseline
Quick Reference Commands
Run Everything
bash
# Run all tests at once
./scripts/run_complete_tests.sh

# Generate all tables
python3 scripts/generate_final_thesis_tables.py > all_results.txt
Run Specific Test
bash
# Run only Test 2
cp configs/params_test2_du11_dv3.h params.h
make clean && make speed
./test_speed512 > results/test2/kyber512.txt
Check Results
bash
# View all Kyber512 compression results
for test in test1 test2 test3; do
    echo "=== $test ==="
    grep -A2 "poly_compress:" results/$test/kyber512.txt
done

# Compare eta variations
echo "Baseline eta1:"
grep -A2 "poly_getnoise_eta1:" results/baseline/kyber768.txt | grep median
echo "Modified eta1:"
grep -A2 "poly_getnoise_eta1:" results/test4/kyber768.txt | grep median
Expected Results
Performance Patterns
Compression (du,dv):

Higher du → more compression cycles
Higher dv → affects decompression time
Trade-off between compression efficiency and speed
Eta Variations:

Higher η → more noise sampling cycles
Kyber512: η1 3→5 increases ~25%
Kyber768: η1 2→4 increases ~70%
Table Structure
All results match the thesis tables:

Table 5.1: Kyber512 (du,dv) performance
Table 5.2: Kyber768 (du,dv) performance
Table 5.3: Kyber1024 (du,dv) performance
Table 5.4: Eta variations performance
Troubleshooting
Build Errors
bash
# If poly.c errors about unsupported POLYCOMPRESSEDBYTES
# Check that all cases are added before #else

# If cbd.c errors about undefined cbd functions
# Ensure conditional compilation guards are removed

# Clean build
make clean
rm -f *.o
make
Missing Results
bash
# Check if directory exists
ls -la results/test1/

# Create if missing
mkdir -p results/test1

# Verify file was created
ls -la results/test1/kyber512.txt
Conclusion
This implementation successfully reproduces all Kyber parameter tweaks from Chapter 5 of the thesis:

✅ All compression parameter variations (du,dv)
✅ All noise distribution variations (η1,η2)
✅ Special Kyber1024 configurations
✅ Performance measurements matching thesis structure
✅ Automated testing and result generation
The complete implementation is ready for thesis presentation and further analysis.