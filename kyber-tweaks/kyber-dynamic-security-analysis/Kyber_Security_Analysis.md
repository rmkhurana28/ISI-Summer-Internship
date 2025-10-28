Kyber Security Analysis - Complete Documentation
Overview
This project provides comprehensive security analysis for the Kyber post-quantum cryptographic scheme. It includes two approaches:

Static Analysis: Uses hardcoded security estimates from thesis research
Dynamic Analysis: Calculates actual security estimates using the Lattice Estimator
Project Structure
text
kyber-security-analysis/
├── kyber-security-analysis/              # Static (hardcoded) analysis
│   ├── scripts/
│   │   ├── kyber_security_analysis.py    # Main static analysis script
│   │   ├── Kyber.py                      # Individual parameter testing
│   │   ├── run_kyber_tests.py           # Test runner
│   │   └── visualize_results.py         # Generate plots
│   ├── results/
│   │   ├── security_analysis_results.txt
│   │   ├── parameter_test_results.txt
│   │   ├── test_result_[5,6,7].txt
│   │   ├── eta_test_results.txt
│   │   └── plots/
│   │       ├── kyber_security_comparison.png
│   │       └── kyber_eta_comparison.png
│   ├── venv/                            # Python virtual environment
│   ├── run_all_analysis.sh              # Master runner script
│   └── requirements.txt
│
└── kyber-dynamic-security-analysis/      # Dynamic (calculated) analysis
    ├── scripts/
    │   ├── dynamic_analyzer.py           # Main dynamic analysis
    │   ├── test_sage_connection.py       # System tests
    │   ├── compare_results.py           # Compare static vs dynamic
    │   ├── visualize_dynamic.py         # Generate plots
    │   └── check_estimator.py          # Check estimator setup
    ├── sage-scripts/
    │   └── kyber_estimator.sage         # SageMath security calculations
    ├── estimator/
    │   └── lattice-estimator/           # Cloned estimator repository
    ├── results/
    │   ├── tables/
    │   │   ├── kyber512_dudv_analysis.txt
    │   │   ├── kyber768_dudv_analysis.txt
    │   │   ├── kyber1024_dudv_analysis.txt
    │   │   └── kyber_eta_analysis.txt
    │   ├── plots/
    │   │   ├── dynamic_security_comparison.png
    │   │   └── dudv_variations.png
    │   ├── complete_results.json
    │   ├── dynamic_analysis_log.txt
    │   └── comparison.txt
    ├── run_dynamic_analysis.sh
    └── setup_dynamic.sh
Installation Guide
Prerequisites
Python 3.7 or higher
Git
SageMath (for dynamic analysis only)
Part 1: Static Analysis Setup
bash
# 1. Clone or create the project directory
mkdir -p kyber-security-analysis
cd kyber-security-analysis

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install numpy matplotlib pandas tabulate

# 4. Create the directory structure
mkdir -p scripts results/plots

# 5. Copy all static analysis scripts to scripts/ directory
# - kyber_security_analysis.py
# - Kyber.py
# - run_kyber_tests.py
# - visualize_results.py

# 6. Copy run_all_analysis.sh to the main directory
chmod +x run_all_analysis.sh
Part 2: Dynamic Analysis Setup
bash
# 1. Go to the dynamic analysis directory
cd ../kyber-dynamic-security-analysis

# 2. Install SageMath (if not already installed)
# Option A: Using apt (Ubuntu/Debian)
sudo apt update
sudo apt install sagemath

# Option B: Using conda
conda create -n sage_env sage python=3.9
conda activate sage_env

# Option C: Download from https://www.sagemath.org/download.html

# 3. Verify SageMath installation
sage --version

# 4. Run setup script
chmod +x setup_dynamic.sh
./setup_dynamic.sh

# 5. Install Python packages in Sage environment
sage -pip install tabulate numpy matplotlib

# 6. Copy all scripts to their directories:
# - Python scripts → scripts/
# - Sage script → sage-scripts/
Running the Analysis
Static Analysis (Hardcoded Values)
bash
cd kyber-security-analysis

# Activate virtual environment
source venv/bin/activate

# Run complete static analysis
./run_all_analysis.sh

# Or run individual components:
python3 scripts/kyber_security_analysis.py  # Main analysis
python3 scripts/Kyber.py --param-set 512 --du 10 --dv 4  # Specific test
python3 scripts/visualize_results.py  # Generate plots
Expected Output:

Security tables matching thesis values
Test results for different parameter configurations
Visualization plots
All results in results/ directory
Dynamic Analysis (Calculated Values)
bash
cd kyber-dynamic-security-analysis

# Ensure SageMath environment is active
conda activate sage_env  # if using conda

# Run complete dynamic analysis
./run_dynamic_analysis.sh

# Or run individual components:
cd scripts
python3 test_sage_connection.py  # Test setup
python3 dynamic_analyzer.py      # Run analysis
python3 visualize_dynamic.py     # Generate plots
python3 compare_results.py ../results/complete_results.json  # Compare results
Expected Output:

Calculated security estimates
Tables showing actual security levels
Comparison with static values
Visualization plots
Troubleshooting
Common Issues and Solutions
1. SageMath Not Found
text
Error: SageMath not found!
Solution: Install SageMath using one of the methods in the installation guide.

2. Module Not Found Error
text
ModuleNotFoundError: No module named 'tabulate'
Solution: Install missing module:

bash
# For static analysis
pip install tabulate

# For dynamic analysis  
sage -pip install tabulate
3. Lattice Estimator Import Error
text
ImportError: cannot import name 'DiscreteGaussianDistribution'
Solution: The import is already fixed in the provided scripts. Make sure you're using the updated kyber_estimator.sage.

4. JSON Serialization Error
text
TypeError: Object of type Integer is not JSON serializable
Solution: This is fixed in the provided scripts by converting Sage types to Python types.

5. Path Not Found
text
No such file or directory: 'scripts/Kyber.py'
Solution: Ensure all scripts are in the correct directories as shown in the structure.

Understanding the Results
Static Analysis Results
The static analysis shows hardcoded values from thesis research:

Variant	(du,dv)	Primal Attack	Dual Attack
Kyber512	(10,4)	118 bits	117 bits
Kyber768	(10,4)	183 bits	181 bits
Kyber1024	(11,5)	256 bits	253 bits
Dynamic Analysis Results
The dynamic analysis calculates actual security using the lattice estimator:

Variant	(du,dv)	Primal Attack	Dual Attack
Kyber512	(10,4)	144 bits	143 bits
Kyber768	(10,4)	212 bits	210 bits
Kyber1024	(11,5)	285 bits	282 bits
Key Differences
Dynamic results show 25-30 bits higher security
This is due to updated algorithms in the lattice estimator
The (du,dv) parameters don't significantly affect security in the dynamic analysis
Security Parameters Explained
n: Polynomial degree (256 for Kyber)
k: Module rank (2/3/4 for Kyber512/768/1024)
η1, η2: Noise distribution parameters
du, dv: Compression parameters
q: Modulus (3329 for Kyber)
Comparison Features
The analysis provides:

Security tables for different parameter sets
Visual comparisons between variants
Static vs Dynamic comparison
Parameter sensitivity analysis
Verifying Results
To verify the analysis is working correctly:

Check log files for any errors
Compare table values with expected ranges
Ensure plots are generated successfully
Verify JSON output contains all expected fields
Advanced Usage
Custom Parameter Analysis
python
# Add custom parameters to dynamic_analyzer.py
custom_params = {
    "n": 256,
    "k": 2,
    "eta1": 4,
    "eta2": 3,
    "q": 3329,
    "du": 11,
    "dv": 4
}
Batch Analysis
bash
# Create a batch script for multiple parameters
for du in 9 10 11 12; do
    for dv in 3 4 5 6; do
        python3 scripts/Kyber.py --param-set 512 --du $du --dv $dv
    done
done
Contact and Support
For issues or questions:

Check the troubleshooting section
Verify all dependencies are installed
Ensure scripts are in correct directories
Check log files for detailed error messages
References
Lattice Estimator: https://github.com/malb/lattice-estimator
Kyber Specification: https://pq-crystals.org/kyber/
SageMath Documentation: https://www.sagemath.org/