# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This repository contains performance optimization implementations for NIST post-quantum cryptographic standards, specifically focusing on Kyber (ML-KEM) parameter tweaks for compression and noise distribution trade-offs. The implementation is based on the thesis Chapter 5 work.

## Working Directory Structure

The Kyber implementation is located at: `kyber-tweaks/kyber/ref/`

```
kyber-tweaks/kyber/ref/
├── configs/                      # Parameter configuration headers
├── results/                      # Test results organized by test
├── scripts/                      # Automation scripts
├── poly.c                       # Modified for compression values
├── polyvec.c                    # Modified for compression values  
├── cbd.c                        # Modified with cbd4, cbd5 functions
├── params.h                     # Current parameter configuration
└── Makefile                     # Build system
```

## Build Commands

### Basic Build Operations

```bash
# Navigate to Kyber directory
cd kyber-tweaks/kyber/ref

# Clean build
make clean && make

# Build speed tests only
make clean && make speed

# Build specific variant
make clean && make test_speed512
make clean && make test_speed768
make clean && make test_speed1024
```

### Configuration Management

```bash
# Switch to specific configuration (Test 1: baseline)
cp configs/params_test1_du10_dv4.h params.h

# Switch to Test 2 configuration (du=11, dv=3)
cp configs/params_test2_du11_dv3.h params.h

# Switch to Test 3 configuration (du=9, dv=5)
cp configs/params_test3_du9_dv5.h params.h

# Switch to Test 4 configuration (eta variations)
cp configs/params_test4_eta_variations.h params.h
```

## Running Tests

### Individual Test Execution

```bash
# Run Test 1 (baseline configuration)
cp configs/params_test1_du10_dv4.h params.h
make clean && make speed
./test_speed512 > results/test1/kyber512.txt
./test_speed768 > results/test1/kyber768.txt
./test_speed1024 > results/test1/kyber1024.txt

# Run Test 2 (du=11, dv=3)
cp configs/params_test2_du11_dv3.h params.h
make clean && make speed
./test_speed512 > results/test2/kyber512.txt
./test_speed768 > results/test2/kyber768.txt
./test_speed1024 > results/test2/kyber1024.txt
```

### Automated Test Suite

```bash
# Run all standard tests (1-4)
./scripts/run_all_tests.sh

# Run complete test suite including special Kyber1024 configs
./scripts/run_complete_tests.sh

# Generate thesis-format tables
python3 scripts/generate_final_thesis_tables.py > final_thesis_tables.txt
```

### Quick Performance Checks

```bash
# View compression performance for Test 1
grep -A2 "poly_compress:" results/test1/kyber512.txt

# Compare compression across all tests
for test in test1 test2 test3; do
    echo "=== $test ==="
    grep -A2 "poly_compress:" results/$test/kyber512.txt | grep median
done

# Check eta variation impact
grep -A2 "poly_getnoise_eta1:" results/test4/kyber768.txt | grep median
```

## Code Architecture

### Key Modified Components

#### 1. Compression Functions (poly.c)
The `poly_compress` and `poly_decompress` functions have been modified to support multiple compression levels:
- 96 bytes (3-bit compression) - for du=11, dv=3
- 128 bytes (4-bit compression) - standard
- 160 bytes (5-bit compression) - standard
- 192 bytes (6-bit compression) - for du=10, dv=6
- 200 bytes (special Kyber1024) - for du=11, dv=5

#### 2. Vector Compression (polyvec.c)
The `polyvec_compress` and `polyvec_decompress` functions support:
- 288*K bytes (9-bit compression)
- 320*K bytes (10-bit compression) - standard
- 352*K bytes (11-bit compression) - standard
- 384*K bytes (12-bit compression)

#### 3. Noise Sampling (cbd.c)
Enhanced CBD (Centered Binomial Distribution) functions:
- `cbd2` - for η=2 (standard)
- `cbd3` - for η=3 (standard)
- `cbd4` - for η=4 (new, for Test 4)
- `cbd5` - for η=5 (new, for Test 4)

The conditional compilation guards have been removed to support all eta values.

### Parameter Configurations

#### Test 1 (Baseline/Standard):
- Kyber512: η1=3, η2=2, du=10, dv=4
- Kyber768: η1=2, η2=2, du=10, dv=4  
- Kyber1024: η1=2, η2=2, du=11, dv=5

#### Test 2 (High Compression):
- All variants: du=11, dv=3
- Trades smaller ciphertext for potential reliability

#### Test 3 (Alternative Balance):
- All variants: du=9, dv=5
- Different compression trade-off point

#### Test 4 (Noise Variations):
- Kyber512: η1=5, η2=3
- Kyber768: η1=4, η2=4
- Kyber1024: η1=4, η2=4

### Key Functions to Monitor

When modifying compression parameters:
1. `poly_compress()` / `poly_decompress()` - polynomial compression
2. `polyvec_compress()` / `polyvec_decompress()` - vector compression
3. `poly_cbd_eta1()` / `poly_cbd_eta2()` - noise sampling
4. `indcpa_keypair()` - key generation
5. `indcpa_enc()` - encapsulation
6. `indcpa_dec()` - decapsulation

## Common Development Tasks

### Adding a New Configuration

```bash
# 1. Create new config file
cp configs/params_test1_du10_dv4.h configs/params_new_config.h

# 2. Edit the parameters in the new file
# Modify KYBER_POLYCOMPRESSEDBYTES and KYBER_POLYVECCOMPRESSEDBYTES

# 3. Create results directory
mkdir -p results/new_test

# 4. Build and test
cp configs/params_new_config.h params.h
make clean && make speed
./test_speed512 > results/new_test/kyber512.txt
```

### Extracting Specific Metrics

```bash
# Extract all poly_compress results
python3 scripts/extract_results.py

# Get specific operation for all tests
for test in test1 test2 test3 test4; do
    echo "$test: $(grep -A2 'indcpa_keypair:' results/$test/kyber512.txt | grep median)"
done
```

### Debugging Build Issues

```bash
# Check undefined compression values
grep KYBER_POLYCOMPRESSEDBYTES params.h

# Verify cbd functions are available
grep "static void cbd" cbd.c

# Check for compilation errors in modified files
gcc -c -Wall poly.c
gcc -c -Wall polyvec.c
gcc -c -Wall cbd.c
```

## Important Implementation Details

### Compression Value Calculation

For Kyber with security parameter k:
- `KYBER_POLYCOMPRESSEDBYTES = 32 * dv` (for polynomial)
- `KYBER_POLYVECCOMPRESSEDBYTES = k * 32 * du` (for vector)

### Performance Measurement

All performance tests use RDTSC cycle counting:
- Measurements taken over multiple iterations
- Results show median and average CPU cycles
- Standard deviation included for variability analysis

### Parameter Constraints

When modifying parameters:
- du ∈ {9, 10, 11, 12} - affects ciphertext size and compression time
- dv ∈ {3, 4, 5, 6} - affects ciphertext size and decompression time
- η ∈ {2, 3, 4, 5} - affects noise sampling time and security

## Expected Performance Patterns

### Compression Impact:
- Higher du → more compression cycles, smaller ciphertext
- Higher dv → more decompression cycles, smaller ciphertext
- Trade-off between size and computational cost

### Eta (Noise) Impact:
- η=3→5: ~25% increase in sampling time for Kyber512
- η=2→4: ~70% increase in sampling time for Kyber768
- Affects key generation and encapsulation performance

## Testing Checklist

When validating changes:
- [ ] All three security levels build (512, 768, 1024)
- [ ] Speed tests complete without errors
- [ ] Results show expected cycle count ranges
- [ ] Compression/decompression are inverses (correctness)
- [ ] Performance changes align with theoretical expectations

## Directory Navigation

Always work from the Kyber reference implementation directory:
```bash
cd /home/meher/Documents/kyber-dilithium-tweaks/kyber-tweaks/kyber/ref
```

## Python Dependencies

Required for analysis scripts:
- matplotlib (for graphs)
- numpy (for statistics)
- tabulate (for tables)

Install with: `pip3 install --user matplotlib numpy tabulate`