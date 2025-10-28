
## Kyber Parameter Tweaks and Security Analysis - Complete Project Documentation
Table of Contents
Project Overview
Complete Project Structure
Installation and Setup
Core Implementation
Benchmarking Suite
CLI Test Tools
Security Analysis
Results and Analysis
Quick Start Guide
Troubleshooting
Project Overview
This comprehensive project implements and analyzes parameter tweaks for the Kyber post-quantum cryptographic scheme, as described in Chapter 5 of the thesis. The project consists of four major components:

Core Kyber Implementation with Parameter Tweaks: Modified Kyber source code supporting various compression and noise distribution parameters
Performance Benchmarking Suite: Automated tools to measure cycle counts and performance impact
CLI Testing Tools: Interactive utilities for encryption/decryption demonstrations
Security Analysis Framework: Both static (hardcoded) and dynamic (calculated) security analysis
Key Features
✅ Support for multiple compression parameters (du, dv)
✅ Configurable noise distribution parameters (η1, η2)
✅ Automated performance benchmarking
✅ Interactive CLI tools for testing
✅ Comprehensive security analysis
✅ Visualization and reporting tools
Complete Project Structure
text
```text
kyber-tweaks/
├── kyber/
│   └── ref/
│       ├── configs/                          # Parameter configuration files
│       │   ├── params_baseline_standard.h   # NIST Round 3 baseline
│       │   ├── params_test1_du10_dv4.h     # Test 1: (du=10, dv=4)
│       │   ├── params_test2_du11_dv3.h     # Test 2: (du=11, dv=3)
│       │   ├── params_test3_du9_dv5.h      # Test 3: (du=9, dv=5)
│       │   ├── params_test4_eta_variations.h # Test 4: eta variations
│       │   ├── params_kyber1024_du11_dv5.h # Kyber1024 special
│       │   ├── params_kyber1024_du10_dv6.h # Kyber1024 special
│       │   └── params_kyber1024_du12_dv4.h # Kyber1024 special
│       ├── poly.c                           # Modified for compression
│       ├── polyvec.c                        # Modified for compression
│       ├── cbd.c                            # Added cbd4, cbd5
│       └── test_speed[512|768|1024]         # Performance test binaries
│
├── benchmarks/                              # Performance analysis
│   ├── run_cycle_counts.sh                  # Main benchmark runner
│   ├── analyze_results.py                   # Generate thesis tables
│   ├── generate_charts.py                   # Create visualizations
│   ├── generate_report.sh                   # HTML report generator
│   ├── statistical_analysis.py              # Statistical analysis
│   ├── literature_comparison.py             # Compare with papers
│   ├── quick_bench.sh                       # Quick testing
│   └── results/                             # Benchmark results
│       └── run_YYYYMMDD_HHMMSS/
│
├── cli-tests/                               # CLI testing tools
│   ├── kyber_keygen                         # Key generation utility
│   ├── kyber_encrypt                        # Encryption utility
│   ├── kyber_decrypt                        # Decryption utility
│   ├── kyber_demo                           # Interactive demo
│   ├── scripts/
│   │   ├── test_all_params.sh             # Test all configurations
│   │   ├── compare_sizes.sh                # Size comparison
│   │   └── demo_tweaks.sh                  # Interactive demo
│   ├── src/                                 # Source files
│   └── Makefile
│
├── kyber-security-analysis/                 # Static security analysis
│   ├── scripts/
│   │   ├── kyber_security_analysis.py      # Main analysis
│   │   ├── Kyber.py                        # Parameter testing
│   │   ├── run_kyber_tests.py             # Test runner
│   │   └── visualize_results.py           # Generate plots
│   ├── results/
│   └── run_all_analysis.sh
│
└── kyber-dynamic-security-analysis/         # Dynamic security analysis
    ├── scripts/
    │   ├── dynamic_analyzer.py              # Dynamic analysis
    │   └── compare_results.py              # Compare results
    ├── sage-scripts/
    │   └── kyber_estimator.sage            # SageMath calculations
    └── results/
```
Installation and Setup
System Requirements
Ubuntu Linux (tested on 24.04.2 LTS)
GCC compiler (version 6.3.0 or higher)
Python 3.7+
Git
SageMath (for dynamic security analysis)
16GB RAM recommended
Complete Setup Process
```bash
# 1. Create main project directory
mkdir kyber-tweaks
cd kyber-tweaks

# 2. Clone and setup Kyber
git clone https://github.com/pq-crystals/kyber
cd kyber
git checkout round3
cd ref

# 3. Apply source modifications (see Core Implementation section)
# Create configs directory
mkdir -p configs

# 4. Setup benchmarking
cd ../..
mkdir -p benchmarks/results

# 5. Setup CLI tests
mkdir -p cli-tests/{src,scripts,examples}

# 6. Setup security analysis
mkdir -p kyber-security-analysis/{scripts,results}
mkdir -p kyber-dynamic-security-analysis/{scripts,sage-scripts,results}

# 7. Install Python dependencies
pip install numpy matplotlib pandas tabulate

# 8. Install SageMath (for security analysis)
sudo apt install sagemath  # or use conda
```
Core Implementation
Modified Source Files
Note: Dynamic results show ~25-30 bits higher security due to updated lattice estimator algorithms.

Security Analysis Features
Parameter Sensitivity Analysis: How (du,dv) and (η1,η2) affect security
Visual Comparisons: Charts showing security across variants
Static vs Dynamic Comparison: Understanding estimation differences
Batch Analysis: Test multiple parameter combinations
Results and Analysis
Performance Impact Summary
1. Compression Parameters (du, dv)
Test 2 (11,3): ~4% ciphertext increase, ~50% compression overhead, minimal overall impact
Test 3 (9,5): ~4% ciphertext decrease, ~100% compression overhead, 10-15% overall impact
Trade-off: Size reduction comes at computational cost
2. Noise Parameters (η1, η2)
Increased η: No ciphertext size change
Performance: Significant impact on key generation and encryption
Security: Provides additional security margin
3. Special Kyber1024 Configurations
(11,5): Uses special 200-byte encoding
(10,6): Shows -5% KeyGen improvement
(12,4): Mixed results, variant-dependent
Verification Results
✅ Correctness: All parameter configurations pass encryption/decryption tests

text
baseline_standard: PASSED
test1_du10_dv4: PASSED
test2_du11_dv3: PASSED
test3_du9_dv5: PASSED
test4_eta_variations: PASSED
✅ Size Impact: Ciphertext sizes match theoretical predictions
✅ Performance Patterns: Cycle counts show expected relative differences
✅ Security Levels: Both static and dynamic analysis confirm security margins

Quick Start Guide
1. Basic Parameter Test
```bash
# From kyber/ref directory
cp configs/params_test2_du11_dv3.h params.h
make clean && make speed
./test_speed512
```
2. Complete Benchmark Run
```bash
cd benchmarks
./run_cycle_counts.sh
python3 analyze_results.py | grep -A20 "Table 5.1"
```
3. Interactive Demo
```bash
cd cli-tests
./kyber_demo
```
4. Security Check
```bash
cd kyber-security-analysis
python3 scripts/kyber_security_analysis.py
```
Troubleshooting
Common Issues and Solutions
1. Build Errors
```bash
# Missing compression cases in poly.c
Error: KYBER_POLYCOMPRESSEDBYTES needs to be in {96, 128, 160, 192, 200}

# Solution: Ensure all cases are added before #else in poly.c
```
2. CBD Function Errors
```bash
# Undefined cbd4 or cbd5
Error: implicit declaration of function 'cbd4'

# Solution: Remove conditional compilation guards in cbd.c
```
3. Path Issues
```bash
# Config file not found
cp: cannot stat 'configs/params_test1_du10_dv4.h': No such file or directory

# Solution: Check you're in correct directory (kyber/ref)
```
4. SageMath Issues
```bash
# SageMath not found
Error: SageMath not found!

# Solution: Install SageMath
sudo apt install sagemath
# or
conda create -n sage_env sage python=3.9
```
5. Python Module Issues
```bash
# Missing Python modules
ModuleNotFoundError: No module named 'tabulate'

# Solution:
pip install tabulate numpy matplotlib pandas
```
Verification Commands
```bash
# Verify all config files exist
ls kyber/ref/configs/params_*.h | wc -l  # Should be 9

# Check modifications are in place
grep -c "KYBER_POLYCOMPRESSEDBYTES == 96" kyber/ref/poly.c  # Should be ≥1
grep -c "cbd4" kyber/ref/cbd.c  # Should be ≥1

# Test CLI tools
cd cli-tests
./scripts/test_all_params.sh  # All should show SUCCESS

# Check benchmark results
cd benchmarks
ls results/run_*/test*/kyber512.txt | wc -l  # Should match number of tests
```
Advanced Usage
Custom Parameter Testing
```bash
# Create custom configuration
cat > kyber/ref/configs/params_custom.h << EOF
// Custom parameters
#define KYBER_ETA1 4
#define KYBER_ETA2 3
// ... other parameters
EOF

# Test custom configuration
cd benchmarks
./run_cycle_counts.sh  # Will pick up new config
```
Batch Performance Analysis
```bash
# Test multiple compression parameters
for du in 9 10 11 12; do
    for dv in 3 4 5 6; do
        # Create config and test
        echo "Testing du=$du, dv=$dv"
    done
done
```
Automated Reporting
```bash
# Generate complete thesis-ready report
cd benchmarks
./run_cycle_counts.sh
python3 analyze_results.py > thesis_tables.txt
./generate_report.sh
cd results/run_*/report
firefox benchmark_report.html
```
Project Workflow
Complete Testing Workflow
Setup and Build
```bash
cd kyber/ref
make clean && make
```
Run Benchmarks
```bash
cd ../../benchmarks
./run_cycle_counts.sh
```
Test Correctness
```bash
cd ../cli-tests
./scripts/test_all_params.sh
```
Analyze Security
```bash
cd ../kyber-security-analysis
./run_all_analysis.sh
```
Generate Reports
```bash
cd ../benchmarks
./generate_report.sh
python3 analyze_results.py
```
Expected Outputs
Benchmark Results Format
text
```text
poly_compress:
  median: 308 cycles/ticks
  average: 312 cycles/ticks
```
CLI Test Output
text
```text
Testing: baseline_standard
Building... ✓
Generating keys... ✓
Encrypting... ✓
Decrypting... ✓
Verifying... ✓ Shared secrets match!
```
Security Analysis Output
text
```text
Kyber512 Security Analysis:
  Primal attack complexity: 144 bits
  Dual attack complexity: 143 bits
  Security level: 128 bits (Level 1)
```
References and Resources
Kyber Specification: https://pq-crystals.org/kyber/
NIST PQC: https://csrc.nist.gov/projects/post-quantum-cryptography
Lattice Estimator: https://github.com/malb/lattice-estimator
SageMath: https://www.sagemath.org/
Conclusion
This comprehensive implementation provides:

Flexible Kyber Implementation: Supporting multiple parameter configurations
Automated Benchmarking: Complete performance analysis with statistical rigor
Interactive Testing: CLI tools for demonstration and verification
Security Validation: Both theoretical and calculated security analysis
Complete Documentation: Ready for thesis presentation
The project successfully demonstrates:

✅ Parameter flexibility in Kyber
✅ Size/performance trade-offs
✅ Security implications of parameter choices
✅ Practical implementation considerations
All components are tested, verified, and ready for academic presentation or further research.



