# Kyber Benchmark Report - Run 20251015_162101

This directory contains the comprehensive benchmark report for Kyber parameter optimization tests.

## Files

- **benchmark_report.html**: Complete HTML report with charts and analysis
- **benchmark_summary.txt**: Text summary of key findings
- **raw_data/**: Directory containing all raw benchmark outputs

## Quick Summary

### Test Configurations
1. **Baseline**: Standard NIST Round 3 Kyber parameters
2. **Compression Tests**: Various (du, dv) parameter combinations
3. **Eta Variations**: Modified noise distribution parameters
4. **Kyber1024 Special**: Additional compression schemes for Kyber1024

### Key Findings
- Compression parameter changes have significant impact on poly_compress operations
- Eta parameter increases notably affect key generation and encryption
- Some parameter combinations show promise for size/performance trade-offs

### Viewing the Report
Open `benchmark_report.html` in a web browser for the full interactive report.

Generated on: Wed Oct 15 04:23:43 PM IST 2025
