# Post-Quantum Cryptographic Parameter Optimizations

## Overview

This repository contains implementations and analysis of parameter optimizations for NIST's post-quantum cryptographic standards: Kyber (KEM) and Dilithium (signatures).

## 📦 Prerequisites

### System Requirements
- Ubuntu 20.04+ (tested on 24.04 LTS)
- GCC 6.3.0+
- Python 3.7+
- 16GB RAM recommended

### Dependencies

```bash
# System packages
sudo apt update
sudo apt install -y build-essential libssl-dev python3-pip git make

# Python packages
pip install numpy>=1.26 matplotlib>=3.8 pandas>=2.1 tabulate>=0.9.0

# Optional: SageMath for dynamic analysis
sudo apt install -y sagemath  # or use conda environment
```

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd kyber-dilithium-tweaks

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
./run_all_demos.sh --auto

# View results
cat combined_results_*.txt
```

## 📂 Project Structure

```
.
├── run_all_demos.sh          # Master script for all analyses
├── kyber-tweaks/             # Kyber optimizations
│   ├── kyber/ref/            # Core implementation
│   ├── benchmarks/           # Performance tests
│   └── cli-tests/            # Correctness tests
└── dilithium_tweaks/         # Dilithium modifications
    ├── dilithium/           # Core implementation
    ├── benchmarks/          # Performance tests
    └── cli-tests/           # Testing tools
```

## 🔍 Key Features

### Kyber Optimizations
- Compression parameter analysis (du, dv)
- Noise distribution studies (η variations)
- 4% ciphertext size reduction with minimal overhead

### Dilithium Modifications
- SHA3-256 integration
- Expanded challenge space
- Two rejection sampling variants

## 📊 Results Summary

### Kyber Performance
| Configuration | Ciphertext Size | Performance Impact |
|---------------|------------------|-------------------|
| (10,4) Baseline | 768/1088/1568 bytes | Reference |
| (11,3) Optimized | -4% | +5% |
| (9,5) Maximum | +4% | +15% |

### Dilithium Performance
| Implementation | Signing Time (median) | 95th Percentile |
|----------------|----------------------|-----------------|
| Baseline | 6.5ms | 7.2ms |
| Option 1 | 11.0ms | 28.5ms |
| Option 2 | 8.7ms | 10.2ms |

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 👥 Authors and Affiliation

- Meher Venkat Raman  (Student ID: 22MCCE01) — University of Hyderabad
- Prajjwal (Student ID: 22MCCE20) — University of Hyderabad
- Ridham Khurana (Student ID: 22MCCE09) — University of Hyderabad
- Shiva Karthikeya (Student ID: 22MCCE26) — University of Hyderabad

### Supervision

This project was completed as part of an internship under the guidance of Subba Rao (Supervisor), University of Hyderabad.

## 📈 Performance Analysis

### Benchmarking Methodology

- **Environment**: Intel Xeon @ 2.800GHz, Ubuntu 24.04 LTS
- **Compiler**: GCC 6.3.0 with `-O3 -fomit-frame-pointer -march=native`
- **Methodology**: Median of 10,000 iterations, TurboBoost disabled
- **Metrics**: CPU cycles, wall-clock time, memory usage

### Key Performance Findings

<details>
<summary><b>Kyber Performance Impact</b></summary>

#### Compression Operations (cycles)
| Operation | (10,4) Baseline | (11,3) Optimized | (9,5) Maximum |
|-----------|-----------------|------------------|---------------|
| poly_compress | 438 | 638 (+46%) | 878 (+100%) |
| poly_decompress | 146 | 486 (+233%) | 582 (+299%) |
| **Total Impact** | **Baseline** | **+5% overall** | **+15% overall** |

#### Complete Operations (cycles)
| Operation | Kyber512 | Kyber768 | Kyber1024 |
|-----------|----------|----------|-----------|
| KeyGen | ~91,000 | ~153,000 | ~242,000 |
| Encapsulation | ~114,000 | ~185,000 | ~324,000 |
| Decapsulation | ~35,000 | ~48,000 | ~64,000 |
</details>

<details>
<summary><b>Dilithium Performance Comparison</b></summary>

| Metric | Baseline | Option 1 | Option 2 |
|--------|----------|----------|----------|
| **Median Signing** | 6.5ms | 11.0ms | 8.7ms |
| **95th Percentile** | 7.2ms | 28.5ms | 10.2ms |
| **Max Observed** | 8.1ms | 42.3ms | 12.8ms |
| **Variance** | Low | Very High | Moderate |
| **Relative Speed** | 1.0x | 0.59x | 0.75x |
</details>

---

## 🔐 Security Evaluation

### Security Validation Approach

1. **Static Analysis**: Pre-computed security estimates based on latest cryptanalysis
2. **Dynamic Analysis**: Real-time calculation using lattice reduction estimates (requires SageMath)
3. **Parameter Sensitivity**: Analysis of security impact from parameter modifications

### Security Levels Maintained

All parameter variations maintain NIST-required security levels:

| Scheme | NIST Level | Classical Security | Quantum Security | Status |
|--------|------------|-------------------|------------------|--------|
| Kyber512 | 1 | ≥128 bits | ≥64 bits | ✅ Maintained |
| Kyber768 | 3 | ≥192 bits | ≥96 bits | ✅ Maintained |
| Kyber1024 | 5 | ≥256 bits | ≥128 bits | ✅ Maintained |
| Dilithium3 | 3 | ≥192 bits | ≥96 bits | ✅ Maintained |

### Security Analysis Results

<details>
<summary><b>Detailed Security Metrics</b></summary>

#### Kyber Security (Core-SVP Hardness)
| Variant | Parameters | Primal Classical | Dual Classical | Primal Quantum | Dual Quantum |
|---------|------------|------------------|----------------|----------------|--------------|
| Kyber512 (10,4) | Standard | 118 bits | 117 bits | 107 bits | 106 bits |
| Kyber512 (11,3) | Optimized | 118 bits | 117 bits | 107 bits | 106 bits |
| Kyber512 (9,5) | Maximum | 118 bits | 117 bits | 107 bits | 106 bits |

**Key Finding**: Compression parameters do not affect security levels.

#### Dynamic vs Static Analysis
- Static estimates: Based on 2022 cryptanalysis
- Dynamic estimates: 25-30 bits higher (more conservative)
- Both confirm security requirements are met
</details>

---

## 🔄 Reproducibility

### Complete Reproduction Steps

```bash
# 1. Setup environment
git clone <repository-url> pqc-optimizations
cd pqc-optimizations
pip install -r requirements.txt

# 2. Run full analysis
./run_all_demos.sh --auto

# 3. Results will be in:
# - combined_results_YYYYMMDD_HHMMSS.txt (summary)
# - kyber-tweaks/thesis_results_*.txt (Kyber details)
# - dilithium_tweaks/dilithium_tweaks_final_report.html (Dilithium report)
```

### Verification Checksums

All results are deterministic. Key outputs for verification:
- Kyber512 (11,3) poly_compress median: 638 cycles
- Dilithium baseline signing median: 6.5ms
- Security levels: All maintain NIST requirements

---

## 📚 Documentation

### Detailed Component Documentation

- **[Kyber Implementation Details](kyber-tweaks/README.md)**: Parameter configurations, modifications, benchmarking suite
- **[Dilithium Tweaks Documentation](dilithium_tweaks/README.md)**: Algorithm modifications, compatibility matrix
- **[Benchmarking Methodology](benchmarks/README.md)**: Measurement techniques, statistical analysis
- **[Security Analysis Framework](kyber-security-analysis/README.md)**: Static and dynamic analysis methods

### Academic Publications

This work corresponds to:
- **Chapter 5**: "Parameter Optimizations for Kyber" - Comprehensive parameter space analysis
- **Chapter 6**: "Cryptographic Tweaks to Dilithium" - Algorithm modifications and evaluation

---


## 📄 License and Acknowledgments

### License

This project is released under the **MIT License**. See [LICENSE](LICENSE) file for details.

The underlying implementations:
- **Kyber**: Public domain (CC0) from pq-crystals.org
- **Dilithium**: Public domain (CC0) from pq-crystals.org

### Acknowledgments

We gratefully acknowledge:

- **Kyber Team**: P. Schwabe, R. Avanzi, J. Bos, L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, J.M. Schanck, G. Seiler, D. Stehlé
- **Dilithium Team**: L. Ducas, E. Kiltz, T. Lepoint, V. Lyubashevsky, P. Schwabe, G. Seiler, D. Stehlé
- **NIST PQC Team**: For the standardization effort
- **Lattice Estimator**: M. Albrecht and contributors
- **Thesis Advisors**: For invaluable guidance and review

### Contact

- **Issues**: Open an issue in this repository
- **Email**: 22mcce01@uohyd.ac.in

---

```markdown
## 🛠️ Troubleshooting

<details>
<summary><b>Common Issues and Solutions</b></summary>

### SageMath Not Found
```bash
# If using conda and sage not found:
conda activate sage_env
# OR install via apt:
sudo apt install sagemath
```

### Build Errors
```bash
# Missing OpenSSL headers:
sudo apt-get install libssl-dev

# GCC version issues:
sudo apt-get install gcc-9 g++-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90
```

### Python Module Issues
```bash
# Missing modules:
pip install -r requirements.txt

# Permission issues:
pip install --user -r requirements.txt
```

### Git Push Issues (Nested Repositories)
```bash
# If unable to push kyber or estimator directories:
# Remove nested .git directories
find kyber-tweaks/ -name ".git" -type d -not -path "./kyber-tweaks/.git" -exec rm -rf {} +

# Re-add directories
git rm -r --cached kyber-tweaks/
git add kyber-tweaks/
git commit -m "Fix nested repository issues"
git push
```

### Large File Errors
```bash
# Find files >100MB
find . -size +100M -type f

# Common large files to exclude:
# - Miniconda installer
# - Compiled binaries
# - Test data
```
</details>

---

## 🚀 Future Work

This research opens several avenues for further investigation:

### Technical Extensions
- **Hardware Implementations**: FPGA/ASIC analysis of parameter trade-offs
- **Side-Channel Analysis**: Impact of parameters on side-channel resistance
- **Hybrid Schemes**: Integration with classical cryptography
- **Embedded Systems**: Optimization for resource-constrained devices

### Research Directions
- **Additional Parameters**: Exploring q, n variations within security bounds
- **Automated Optimization**: Machine learning for parameter selection
- **Real-World Protocols**: Integration with TLS, SSH, VPN
- **Quantum Resistance**: Analysis under evolving quantum threats

---

## 🤝 Contributing

We welcome contributions to extend this research:

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-optimization`)
3. **Commit** your changes (`git commit -am 'Add new parameter analysis'`)
4. **Push** to the branch (`git push origin feature/new-optimization`)
5. **Create** a Pull Request

### Contribution Guidelines
- Maintain compatibility with existing parameter sets
- Include comprehensive benchmarks for new configurations
- Document security implications
- Add appropriate test cases
- Follow existing code style

### Areas for Contribution
- Additional parameter configurations
- Performance optimizations
- Platform-specific implementations
- Documentation improvements
- Security analysis extensions

---

## 📊 Appendix: Detailed Metrics

### Cycle Count Comparison (Median Values)

<details>
<summary><b>Kyber512 Complete Metrics</b></summary>

| Operation | Baseline | (11,3) | Change | (9,5) | Change |
|-----------|----------|--------|--------|-------|--------|
| poly_compress | 438 | 638 | +45.7% | 878 | +100.5% |
| poly_decompress | 146 | 486 | +232.9% | 582 | +298.6% |
| polyvec_compress | 1818 | 2162 | +18.9% | 2202 | +21.1% |
| polyvec_decompress | 1400 | 1422 | +1.6% | 1388 | -0.9% |
| indcpa_keypair | 90868 | 91738 | +1.0% | 95892 | +5.5% |
| indcpa_enc | 113626 | 119824 | +5.5% | 127896 | +12.6% |
| indcpa_dec | 35406 | 36828 | +4.0% | 40498 | +14.4% |
</details>

<details>
<summary><b>Dilithium3 Timing Distribution</b></summary>

```
Baseline Distribution:
- Min: 5.8ms
- 25th percentile: 6.2ms
- Median: 6.5ms
- 75th percentile: 6.8ms
- 95th percentile: 7.2ms
- Max: 8.1ms

Option 2 Distribution:
- Min: 7.9ms
- 25th percentile: 8.4ms
- Median: 8.7ms
- 75th percentile: 9.1ms
- 95th percentile: 10.2ms
- Max: 12.8ms
```
</details>

---

## 📱 Quick Reference Card

### Essential Commands
```bash
# Complete analysis
./run_all_demos.sh --auto

# Individual components
./run_all_demos.sh --kyber       # Kyber only
./run_all_demos.sh --dilithium   # Dilithium only

# Quick tests
cd kyber-tweaks && ./final_demo.sh --quick
cd dilithium_tweaks && ./cli-tests/cli_demo

# View results
cat combined_results_*.txt
firefox */benchmark_report.html
```

### Key Files and Locations
- **Main Results**: `combined_results_TIMESTAMP.txt`
- **Kyber Reports**: `kyber-tweaks/benchmarks/results/run_*/`
- **Dilithium Reports**: `dilithium_tweaks/dilithium_tweaks_final_report.html`
- **Security Analysis**: `kyber-tweaks/*/results/`
- **Logs**: `*demo_*.log`

### Parameter Quick Reference
```
Kyber Optimal: (du=11, dv=3) - 4% smaller, 5% slower
Dilithium Best: Option 2 - 1.4x slower, consistent
Security: All configurations maintain NIST levels
```

---

## 🙏 Final Notes

This implementation represents a comprehensive exploration of post-quantum cryptographic parameter optimization. While maintaining all security requirements, we've demonstrated meaningful trade-offs that can benefit real-world deployments.

**Remember**: This is research code. For production use, please refer to official NIST-approved implementations and conduct appropriate security reviews.

---

<p align="center">
<b>Thank you for your interest in this research!</b><br>
If you find this work useful, please consider citing it in your research.
</p>

<p align="center">
<i>Last Updated: October 2025 | Version 1.0.0</i>
</p>
```
