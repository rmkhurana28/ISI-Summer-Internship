#!/usr/bin/env python3
import sys

print("\n=== Dilithium Performance Comparison ===\n")
print("Operation        Original      Tweaked       Change")
print("-" * 55)

# Results from your thesis Table 6.1
original = {
    "Keypair": 302250,
    "Sign": 1375222,
    "Verify": 328608
}

# Your tweaked results
tweaked = {
    "Keypair": 316031,
    "Sign": 8009496,
    "Verify": 305817
}

for op in ["Keypair", "Sign", "Verify"]:
    orig = original[op]
    tweak = tweaked[op]
    change = ((tweak - orig) / orig) * 100
    print(f"{op:<15} {orig:>10,} {tweak:>12,}   {change:+6.1f}%")

print("\nAnalysis:")
print("- Keypair generation: Slight increase (~4.6%)")
print("- Signing: Significant increase (~482%) due to SHA256 and rejection changes")
print("- Verification: Slight decrease (~-6.9%)")
print("\nThese results align with Table 6.1 in the thesis.")
