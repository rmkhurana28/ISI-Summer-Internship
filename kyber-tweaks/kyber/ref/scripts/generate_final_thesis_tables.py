#!/usr/bin/env python3

import os
import re

def extract_value(file_path, metric):
    """Extract median and average values for a given metric from a result file."""
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

# Table 5.1: Kyber512 (du,dv) variations
print("Table 5.1: Performance analysis of Kyber512 for different (du, dv) values")
print("-" * 100)
print(f"{'Operation':<20} {'(du,dv)=(10,4)':<30} {'(du,dv)=(11,3)':<30} {'(du,dv)=(9,5)':<30}")
print(f"{'':20} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15}")
print("-" * 100)

operations = ["poly_compress", "poly_decompress", "polyvec_compress", "polyvec_decompress", 
              "indcpa_keypair", "indcpa_enc", "indcpa_dec"]

for op in operations:
    row = f"{op:<20}"
    
    # Test 1: (10,4)
    med, avg = extract_value("results/test1/kyber512.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # Test 2: (11,3)
    med, avg = extract_value("results/test2/kyber512.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # Test 3: (9,5)
    med, avg = extract_value("results/test3/kyber512.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    print(row)

# Table 5.2: Kyber768 (du,dv) variations
print("\n\nTable 5.2: Performance analysis of Kyber768 for different (du, dv) values")
print("-" * 100)
print(f"{'Operation':<20} {'(du,dv)=(10,4)':<30} {'(du,dv)=(11,3)':<30} {'(du,dv)=(9,5)':<30}")
print(f"{'':20} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15}")
print("-" * 100)

for op in operations:
    row = f"{op:<20}"
    
    # Test 1: (10,4)
    med, avg = extract_value("results/test1/kyber768.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # Test 2: (11,3)
    med, avg = extract_value("results/test2/kyber768.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # Test 3: (9,5)
    med, avg = extract_value("results/test3/kyber768.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    print(row)

# Table 5.3: Kyber1024 (du,dv) variations - NEW parameter sets
print("\n\nTable 5.3: Performance analysis of Kyber1024 for different (du, dv) values")
print("-" * 100)
print(f"{'Operation':<20} {'(du,dv)=(11,5)':<30} {'(du,dv)=(10,6)':<30} {'(du,dv)=(12,4)':<30}")
print(f"{'':20} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15} {'Median':<15}{'Average':<15}")
print("-" * 100)

for op in operations:
    row = f"{op:<20}"
    
    # (11,5)
    med, avg = extract_value("results/kyber1024_du11_dv5/results.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # (10,6)
    med, avg = extract_value("results/kyber1024_du10_dv6/results.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    # (12,4)
    med, avg = extract_value("results/kyber1024_du12_dv4/results.txt", op)
    row += f"{med:<15}{avg:<15}"
    
    print(row)

# Table 5.4: Eta variations
print("\n\nTable 5.4: Performance analysis of Kyber with different η1, η2 values")
print("-" * 90)
print(f"{'':20} {'':20} {'Tη1':<15} {'Tη2':<15} {'KeyGen':<15} {'Enc':<15}")
print("-" * 90)

# Kyber512 baseline (same as standard)
eta1_med, eta1_avg = extract_value("results/test1/kyber512.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/test1/kyber512.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/test1/kyber512.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/test1/kyber512.txt", "indcpa_enc")
print(f"{'Kyber512':<20} {'(η1=3, η2=2)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")

# Kyber512 modified
eta1_med, eta1_avg = extract_value("results/test4/kyber512.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/test4/kyber512.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/test4/kyber512.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/test4/kyber512.txt", "indcpa_enc")
print(f"{'':20} {'(η1=5, η2=3)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")

# Kyber768 baseline - USE BASELINE RESULTS
eta1_med, eta1_avg = extract_value("results/baseline/kyber768.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/baseline/kyber768.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/baseline/kyber768.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/baseline/kyber768.txt", "indcpa_enc")
print(f"{'Kyber768':<20} {'(η1=2, η2=2)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")

# Kyber768 modified
eta1_med, eta1_avg = extract_value("results/test4/kyber768.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/test4/kyber768.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/test4/kyber768.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/test4/kyber768.txt", "indcpa_enc")
print(f"{'':20} {'(η1=4, η2=4)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")

# Kyber1024 baseline - USE BASELINE RESULTS
eta1_med, eta1_avg = extract_value("results/baseline/kyber1024.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/baseline/kyber1024.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/baseline/kyber1024.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/baseline/kyber1024.txt", "indcpa_enc")
print(f"{'Kyber1024':<20} {'(η1=2, η2=2)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")

# Kyber1024 modified
eta1_med, eta1_avg = extract_value("results/test4/kyber1024.txt", "poly_getnoise_eta1")
eta2_med, eta2_avg = extract_value("results/test4/kyber1024.txt", "poly_getnoise_eta2")
kg_med, kg_avg = extract_value("results/test4/kyber1024.txt", "indcpa_keypair")
enc_med, enc_avg = extract_value("results/test4/kyber1024.txt", "indcpa_enc")
print(f"{'':20} {'(η1=4, η2=4)':<20} {eta1_med:<15} {eta2_med:<15} {kg_med:<15} {enc_med:<15}")