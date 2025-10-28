#!/usr/bin/env python3
"""
Analyze Kyber benchmark results and generate performance comparison tables
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
import statistics

def parse_cycle_counts(filepath):
    """Extract cycle counts from test_speed output file"""
    results = {}
    
    # Operations to extract (matching your thesis tables)
    operations = [
        'poly_compress',
        'poly_decompress', 
        'polyvec_compress',
        'polyvec_decompress',
        'poly_getnoise_eta1',
        'poly_getnoise_eta2',
        'indcpa_keypair',
        'indcpa_enc',
        'indcpa_dec',
        'crypto_kem_keypair',
        'crypto_kem_enc',
        'crypto_kem_dec'
    ]
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        for op in operations:
            # Look for pattern: operation_name: ... median: XXX, average: YYY
            pattern = rf"{op}[:\s]+.*?median:\s*(\d+).*?average:\s*(\d+)"
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            
            if match:
                results[op] = {
                    'median': int(match.group(1)),
                    'average': int(match.group(2))
                }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return results

def analyze_run_directory(run_dir):
    """Analyze all results in a benchmark run directory"""
    run_data = {
        'timestamp': os.path.basename(run_dir).replace('run_', ''),
        'tests': {}
    }
    
    # Process each test subdirectory
    for test_dir in sorted(os.listdir(run_dir)):
        test_path = os.path.join(run_dir, test_dir)
        
        if os.path.isdir(test_path) and test_dir != 'summary.txt':
            test_data = {
                'metadata': {},
                'results': {}
            }
            
            # Read metadata
            metadata_file = os.path.join(test_path, 'metadata.txt')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    for line in f:
                        if ':' in line:
                            key, value = line.strip().split(':', 1)
                            test_data['metadata'][key.strip()] = value.strip()
            
            # Process each Kyber variant
            for variant in ['512', '768', '1024']:
                result_file = os.path.join(test_path, f'kyber{variant}.txt')
                if os.path.exists(result_file):
                    test_data['results'][f'kyber{variant}'] = parse_cycle_counts(result_file)
            
            run_data['tests'][test_dir] = test_data
    
    return run_data

def generate_comparison_tables(run_data):
    """Generate thesis-style comparison tables"""
    
    # Define test groupings matching thesis structure
    compression_tests = {
        'test1_compression_du10_dv4': '(10, 4)',
        'test2_compression_du11_dv3': '(11, 3)', 
        'test3_compression_du9_dv5': '(9, 5)'
    }
    
    kyber1024_special = {
        'kyber1024_special_du11_dv5': '(11, 5)',
        'kyber1024_special_du10_dv6': '(10, 6)',
        'kyber1024_special_du12_dv4': '(12, 4)'
    }
    
    # Table 5.1: Kyber512 compression analysis
    print("\n" + "="*80)
    print("Table 5.1: Performance analysis of Kyber512 for different (du, dv) values")
    print("="*80)
    print(f"{'Operation':<25} ", end='')
    for test_name, params in compression_tests.items():
        print(f"| (du, dv) = {params:<8} ", end='')
    print("\n" + " "*25, end='')
    for _ in compression_tests:
        print(f"| {'Median':<8} {'Average':<8} ", end='')
    print("\n" + "-"*80)
    
    # Key operations for compression analysis
    key_ops = ['poly_compress', 'poly_decompress', 'polyvec_compress', 
               'polyvec_decompress', 'indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    
    for op in key_ops:
        print(f"{op:<25} ", end='')
        for test_name in compression_tests:
            if test_name in run_data['tests']:
                results = run_data['tests'][test_name]['results'].get('kyber512', {})
                if op in results:
                    median = results[op]['median']
                    avg = results[op]['average']
                    print(f"| {median:<8} {avg:<8} ", end='')
                else:
                    print(f"| {'--':<8} {'--':<8} ", end='')
            else:
                print(f"| {'N/A':<8} {'N/A':<8} ", end='')
        print()
    
    # Table 5.2: Kyber768 compression analysis
    print("\n" + "="*80)
    print("Table 5.2: Performance analysis of Kyber768 for different (du, dv) values")
    print("="*80)
    print(f"{'Operation':<25} ", end='')
    for test_name, params in compression_tests.items():
        print(f"| (du, dv) = {params:<8} ", end='')
    print("\n" + " "*25, end='')
    for _ in compression_tests:
        print(f"| {'Median':<8} {'Average':<8} ", end='')
    print("\n" + "-"*80)
    
    for op in key_ops:
        print(f"{op:<25} ", end='')
        for test_name in compression_tests:
            if test_name in run_data['tests']:
                results = run_data['tests'][test_name]['results'].get('kyber768', {})
                if op in results:
                    median = results[op]['median']
                    avg = results[op]['average']
                    print(f"| {median:<8} {avg:<8} ", end='')
                else:
                    print(f"| {'--':<8} {'--':<8} ", end='')
            else:
                print(f"| {'N/A':<8} {'N/A':<8} ", end='')
        print()
    
    # Table 5.3: Kyber1024 special configurations
    print("\n" + "="*80)
    print("Table 5.3: Performance analysis of Kyber1024 for different (du, dv) values")
    print("="*80)
    print(f"{'Operation':<25} ", end='')
    for test_name, params in kyber1024_special.items():
        print(f"| (du, dv) = {params:<8} ", end='')
    print("\n" + " "*25, end='')
    for _ in kyber1024_special:
        print(f"| {'Median':<8} {'Average':<8} ", end='')
    print("\n" + "-"*80)
    
    for op in key_ops:
        print(f"{op:<25} ", end='')
        for test_name in kyber1024_special:
            if test_name in run_data['tests']:
                results = run_data['tests'][test_name]['results'].get('kyber1024', {})
                if op in results:
                    median = results[op]['median']
                    avg = results[op]['average']
                    print(f"| {median:<8} {avg:<8} ", end='')
                else:
                    print(f"| {'--':<8} {'--':<8} ", end='')
            else:
                print(f"| {'N/A':<8} {'N/A':<8} ", end='')
        print()
    
    # Table 5.4: Eta variations
    print("\n" + "="*80)
    print("Table 5.4: Performance analysis of Kyber with different η1, η2 values")
    print("="*80)
    
    # Extract eta timings
    if 'baseline_standard' in run_data['tests'] and 'test4_eta_variations' in run_data['tests']:
        print(f"{'Variant':<15} {'Configuration':<20} {'Tη1':<10} {'Tη2':<10} {'KeyGen':<10} {'Enc':<10}")
        print("-"*80)
        
        for variant in ['512', '768', '1024']:
            kyber_variant = f'kyber{variant}'
            
            # Baseline
            baseline = run_data['tests']['baseline_standard']['results'].get(kyber_variant, {})
            if baseline:
                eta1 = baseline.get('poly_getnoise_eta1', {}).get('median', '--')
                eta2 = baseline.get('poly_getnoise_eta2', {}).get('median', '--')
                keygen = baseline.get('indcpa_keypair', {}).get('median', '--')
                enc = baseline.get('indcpa_enc', {}).get('median', '--')
                
                # Determine baseline eta values based on variant
                if variant == '512':
                    eta_config = "(η1 = 3, η2 = 2)"
                else:
                    eta_config = "(η1 = 2, η2 = 2)"
                
                print(f"Kyber{variant:<11} {eta_config:<20} {eta1:<10} {eta2:<10} {keygen:<10} {enc:<10}")
            
            # Modified eta
            modified = run_data['tests']['test4_eta_variations']['results'].get(kyber_variant, {})
            if modified:
                eta1 = modified.get('poly_getnoise_eta1', {}).get('median', '--')
                eta2 = modified.get('poly_getnoise_eta2', {}).get('median', '--')
                keygen = modified.get('indcpa_keypair', {}).get('median', '--')
                enc = modified.get('indcpa_enc', {}).get('median', '--')
                
                # Modified eta values from thesis
                if variant == '512':
                    eta_config = "(η1 = 5, η2 = 3)"
                elif variant == '768':
                    eta_config = "(η1 = 4, η2 = 4)"
                else:
                    eta_config = "(η1 = 4, η2 = 4)"
                
                print(f"Kyber{variant:<11} {eta_config:<20} {eta1:<10} {eta2:<10} {keygen:<10} {enc:<10}")

def generate_performance_summary(run_data):
    """Generate performance summary comparing to baseline"""
    print("\n" + "="*80)
    print("PERFORMANCE IMPACT SUMMARY")
    print("="*80)
    
    if 'baseline_standard' not in run_data['tests']:
        print("Baseline not found!")
        return
    
    baseline_data = run_data['tests']['baseline_standard']['results']
    
    # Compare each test to baseline
    for test_name, test_data in run_data['tests'].items():
        if test_name == 'baseline_standard':
            continue
            
        print(f"\nTest: {test_name}")
        if 'Description' in test_data['metadata']:
            print(f"Description: {test_data['metadata']['Description']}")
        
        for variant in ['kyber512', 'kyber768', 'kyber1024']:
            if variant in test_data['results'] and variant in baseline_data:
                print(f"\n  {variant.upper()}:")
                
                # Compare key operations
                ops_to_compare = ['poly_compress', 'indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
                for op in ops_to_compare:
                    if op in test_data['results'][variant] and op in baseline_data[variant]:
                        baseline_val = baseline_data[variant][op]['median']
                        test_val = test_data['results'][variant][op]['median']
                        change = ((test_val - baseline_val) / baseline_val) * 100
                        
                        print(f"    {op:<20}: {test_val:>7} cycles ({change:+.1f}% vs baseline)")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Analyze specific run
        run_dir = sys.argv[1]
    else:
        # Find most recent run
        results_dir = "./results"
        if not os.path.exists(results_dir):
            print("Error: No results directory found!")
            sys.exit(1)
        
        runs = [d for d in os.listdir(results_dir) if d.startswith('run_')]
        if not runs:
            print("Error: No benchmark runs found!")
            sys.exit(1)
        
        # Sort by timestamp and get the most recent
        runs.sort()
        run_dir = os.path.join(results_dir, runs[-1])
        print(f"Analyzing most recent run: {runs[-1]}")
    
    # Check if run directory exists
    if not os.path.exists(run_dir):
        print(f"Error: Directory {run_dir} not found!")
        sys.exit(1)
    
    # Analyze the run
    print(f"\nAnalyzing benchmark results from: {run_dir}")
    run_data = analyze_run_directory(run_dir)
    
    # Generate outputs
    generate_comparison_tables(run_data)
    generate_performance_summary(run_data)
    
    # Save analysis to file
    output_file = os.path.join(run_dir, "analysis_report.txt")
    print(f"\nSaving analysis to: {output_file}")
    
    # Redirect stdout to file and regenerate
    original_stdout = sys.stdout
    with open(output_file, 'w') as f:
        sys.stdout = f
        generate_comparison_tables(run_data)
        generate_performance_summary(run_data)
    sys.stdout = original_stdout
    
    # Save JSON data for further processing
    json_file = os.path.join(run_dir, "analysis_data.json")
    with open(json_file, 'w') as f:
        # Convert to serializable format
        serializable_data = json.dumps(run_data, indent=2)
        f.write(serializable_data)
    
    print(f"JSON data saved to: {json_file}")
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
    