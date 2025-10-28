## Dilithium Cryptographic Tweaks Implementation

This repository contains an implementation of cryptographic tweaks to the Dilithium post-quantum digital signature scheme, demonstrating three variants with different performance/security trade-offs.

### Quick Start
```bash
# Clone and navigate to the project
cd dilithium_tweaks

# Run the complete demonstration
./final_demo.sh

# View results in your browser
firefox benchmarks/benchmark_comprehensive_report.html
```

### What's Implemented
Baseline: Original Dilithium-3 reference implementation
Option 1: All tweaks with relaxed rejection bounds (2×BETA) - 1.7x slower
Option 2: All tweaks with probabilistic bypass (10% acceptance) - 1.4x slower

### Cryptographic Tweaks
SHA3-256 replaces SHAKE256 for challenge generation
Challenge coefficients expanded from {-1,0,1} to {-2,-1,0,1,2}
Modified rejection sampling (two variants)

### Directory Structure
```text
dilithium_tweaks/
├── dilithium/          # Core Dilithium implementation with tweaks
├── benchmarks/         # Performance benchmarking tools
├── cli-tests/          # Command-line testing tools
├── final_demo.sh       # Complete demonstration script
└── generate_final_report.sh  # HTML report generator
```

### Basic Usage
#### Run Complete Demo
```bash
./final_demo.sh
```
This runs all tests, benchmarks, and generates a comprehensive report.

#### Generate HTML Report
```bash
./generate_final_report.sh
firefox dilithium_tweaks_final_report.html
```

#### Quick Test
```bash
cd cli-tests
make -f Makefile.tweaks test_tweaks
```

### Requirements
GCC compiler
OpenSSL development libraries (libssl-dev)
Make
Linux/Unix environment
```bash
# Ubuntu/Debian
sudo apt-get install build-essential libssl-dev

# Fedora
sudo dnf install gcc openssl-devel make
```

### Detailed Testing Walkthrough
1. Initial Setup and Compilation
```bash
# Navigate to the project directory
cd /path/to/dilithium_tweaks

# Compile all components
cd dilithium
make clean && make

cd ../benchmarks
make -f Makefile clean
gcc -O3 -o benchmark_baseline benchmark_comprehensive.c ../dilithium/sign.c ../dilithium/packing.c ../dilithium/polyvec.c ../dilithium/poly.c ../dilithium/ntt.c ../dilithium/reduce.c ../dilithium/rounding.c ../dilithium/fips202.c ../dilithium/symmetric-shake.c ../dilithium/randombytes.c -lm

gcc -O3 -o benchmark_option1 benchmark_comprehensive.c ../dilithium/sign_tweaked.c ../dilithium/packing.c ../dilithium/polyvec.c ../dilithium/poly_tweaked.c ../dilithium/ntt.c ../dilithium/reduce.c ../dilithium/rounding.c ../dilithium/fips202.c ../dilithium/symmetric-shake.c ../dilithium/randombytes.c -lssl -lcrypto -lm

gcc -O3 -o benchmark_option2 benchmark_comprehensive.c ../dilithium/sign_tweaked_prob.c ../dilithium/packing.c ../dilithium/polyvec.c ../dilithium/poly_tweaked.c ../dilithium/ntt.c ../dilithium/reduce.c ../dilithium/rounding.c ../dilithium/fips202.c ../dilithium/symmetric-shake.c ../dilithium/randombytes.c -lssl -lcrypto -lm

cd ../cli-tests
make -f Makefile.tweaks all
```
2. Verify Implementation
```bash
# Check that tweaks are implemented correctly
cd ../dilithium

# Verify Tweak 1: SHA3-256
grep -n "EVP_sha3_256" poly_tweaked.c
# Expected: Lines 504, 541

# Verify Tweak 2: Coefficient expansion
grep -n "(signs & 7) % 5 - 2" poly_tweaked.c
# Expected: Line 554

# Verify Tweak 3 Option 1: Relaxed bounds
grep -n "BETA\*2" sign_tweaked.c
# Expected: Lines 163, 173

# Verify Tweak 3 Option 2: Probabilistic bypass
grep -n "bypass % 10" sign_tweaked_prob.c
# Expected: Lines 166, 182
```
3. Run Individual Tests
A. Core Dilithium Tests
```bash
cd dilithium
./test/test_dilithium3     # Test baseline implementation
./test/test_vectors3        # NIST test vectors
```
B. Benchmark Tests
```bash
cd ../benchmarks

# Run baseline benchmark
./benchmark_baseline
# Expected: ~500k-600k cycles for signing

# Run Option 1 benchmark (slower, high variance)
./benchmark_option1
# Expected: ~2.5M-3M cycles (5-6x slower)

# Run Option 2 benchmark (moderate overhead)
./benchmark_option2
# Expected: ~700k-800k cycles (1.2-1.4x slower)
```
C. CLI Interactive Tests
```bash
cd ../cli-tests

# Generate a key pair
./cli_keygen_simple -o test_key -v

# Create test message
echo "Test message for Dilithium" > message.txt

# Sign with each implementation
./cli_sign_baseline -i message.txt -k output/keys/test_key.sk -o baseline.sig -m baseline -v
./cli_sign_option1 -i message.txt -k output/keys/test_key.sk -o option1.sig -m option1 -v
./cli_sign_option2 -i message.txt -k output/keys/test_key.sk -o option2.sig -m option2 -v

# Verify signatures (matched pairs)
./cli_verify -i message.txt -s output/signatures/baseline.sig -k output/keys/test_key.pk
./cli_verify_option1 message.txt output/signatures/option1.sig output/keys/test_key.pk
./cli_verify_option2 message.txt output/signatures/option2.sig output/keys/test_key.pk

# Test cross-verification (should fail)
./cli_verify -i message.txt -s output/signatures/option1.sig -k output/keys/test_key.pk
# Expected: INVALID SIGNATURE
```
4. Performance Analysis
```bash
# Run comprehensive benchmark (100 iterations)
./cli_benchmark_detailed

# Compare implementations side-by-side
./cli_compare message.txt output/keys/test_key.sk

# Test with different message sizes
./cli_sign_baseline -i test_data/messages/short.txt -k output/keys/test_key.sk -o short.sig -m baseline
./cli_sign_baseline -i test_data/messages/large.txt -k output/keys/test_key.sk -o large.sig -m baseline
```
5. Generate Reports
```bash
# Go back to main directory
cd ..

# Generate comprehensive HTML report
./generate_final_report.sh

# View reports
firefox dilithium_tweaks_final_report.html
firefox benchmarks/benchmark_comprehensive_report.html
```
6. Automated Test Suite
```bash
# Run the complete automated demo
./final_demo.sh

# Run specific test suites
cd cli-tests
make -f Makefile.tweaks test_tweaks        # Basic functionality test
make -f Makefile.tweaks test_performance   # Performance comparison
make -f Makefile.tweaks benchmark          # Detailed benchmark
```

### Expected Results
Performance Impact:

Baseline: ~6.5ms median signing time
Option 1: ~11ms median (high variance, up to 40ms)
Option 2: ~8.7ms median (consistent performance)
Signature Characteristics:

All implementations: 3309-byte signatures
Key sizes: 1952 bytes (public), 4032 bytes (secret)
Compatibility Matrix:

text
Signer    | Baseline | Option 1 | Option 2
----------|----------|----------|----------
Baseline  |    ✓     |    ✗     |    ✗
Option 1  |    ✗     |    ✓     |    ✗
Option 2  |    ✗     |    ✗     |    ✓

### Troubleshooting
Compilation Errors:

```bash
# Missing OpenSSL headers
sudo apt-get install libssl-dev
```
Performance Variations:

```bash
# Disable CPU frequency scaling for consistent results
sudo cpupower frequency-set --governor performance
```
Verification Failures:

Ensure matched signer/verifier pairs
Check file paths are correct
Verify key files exist

### Advanced Testing
For researchers wanting to explore further:

```bash
# Modify rejection parameters
vim dilithium/sign_tweaked.c
# Change BETA*2 to BETA*3 for even more relaxed bounds

# Test specific scenarios
for i in {1..100}; do
    ./cli_sign_option1 -i message.txt -k output/keys/test_key.sk -o test_$i.sig -m option1
done
# Analyze timing variations

# Generate performance profiles
perf record ./benchmark_option1
perf report
```

### Summary
This implementation successfully demonstrates cryptographic tweaks to Dilithium with measurable performance impacts while maintaining security properties. Option 2 (probabilistic bypass) provides the best balance of features and performance for practical applications.

For detailed analysis, see the generated HTML reports and the thesis Chapter 6: "Tweaks to Dilithium".