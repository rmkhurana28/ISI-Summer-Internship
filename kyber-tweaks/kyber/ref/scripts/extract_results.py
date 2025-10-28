#!/usr/bin/env python3

import os
import re
import sys

# Operations to extract
operations = [
    "poly_compress",
    "poly_decompress", 
    "polyvec_compress",
    "polyvec_decompress",
    "indcpa_keypair",
    "indcpa_enc",
    "indcpa_dec"
]

# Test configurations
tests = {
    "test1": "(du=10, dv=4)",
    "test2": "(du=11, dv=3)",
    "test3": "(du=9, dv=5)",
    "test4": "eta variations"
}

def extract_value(file_path, metric):
    """Extract median and average values for a given metric from a result file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Use raw string to avoid escape sequence warning
            pattern = rf"{metric}:.*?median: (\d+).*?average: (\d+)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1), match.group(2)
    except:
        pass
    return "N/A", "N/A"

def print_results_table(variant, test_list=None):
    """Print results table for a specific Kyber variant."""
    if test_list is None:
        test_list = ["test1", "test2", "test3", "test4"]
    
    print(f"\n{variant.upper()} Results:")
    print("-" * 100)
    
    # Header
    header = f"{'Operation':<25}"
    for test in test_list:
        test_desc = tests.get(test, test)
        header += f"{test_desc:<25}"
    print(header)
    print("-" * 100)
    
    # Data rows
    for op in operations:
        row = f"{op:<25}"
        for test in test_list:
            filepath = f"results/{test}/{variant}.txt"
            if os.path.exists(filepath):
                median, avg = extract_value(filepath, op)
                row += f"{median:>8} / {avg:<15}"
            else:
                row += f"{'Missing':<25}"
        print(row)

def main():
    # Check if results directory exists
    if not os.path.exists("results"):
        print("Error: results directory not found!")
        print("Please run the tests first using: ./scripts/run_all_tests.sh")
        sys.exit(1)
    
    # Extract results for standard tests
    for variant in ["kyber512", "kyber768", "kyber1024"]:
        print_results_table(variant)
    
    # Check for Kyber1024 special configurations
    special_tests = []
    for dirname in ["kyber1024_du11_dv5", "kyber1024_du10_dv6", "kyber1024_du12_dv4"]:
        if os.path.exists(f"results/{dirname}/results.txt"):
            special_tests.append(dirname)
    
    if special_tests:
        print("\n" + "="*100)
        print("KYBER1024 Special Configurations:")
        print("="*100)
        
        header = f"{'Operation':<25}"
        for test in special_tests:
            header += f"{test:<35}"
        print(header)
        print("-" * 100)
        
        for op in operations:
            row = f"{op:<25}"
            for test in special_tests:
                filepath = f"results/{test}/results.txt"
                median, avg = extract_value(filepath, op)
                if median != "N/A":
                    row += f"{median:>8} / {avg:<25}"
                else:
                    row += f"{'N/A':<35}"
            print(row)

if __name__ == "__main__":
    main()