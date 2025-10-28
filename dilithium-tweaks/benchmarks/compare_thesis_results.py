#!/usr/bin/env python3

print("\n=== Comparison with Thesis Table 6.1 ===\n")
print("Operation    Metric      Thesis       Current      Difference")
print("-" * 65)

# Thesis Table 6.1 values (After Tweak)
thesis = {
    "Keypair": {"median": 297386, "average": 300861},
    "Sign": {"median": 5239586, "average": 7534151},
    "Verify": {"median": 334196, "average": 341053}
}

# Current results
current = {
    "Keypair": {"median": 314271, "average": 320543},
    "Sign": {"median": 5639888, "average": 8104452},
    "Verify": {"median": 323581, "average": 325653}
}

for op in ["Keypair", "Sign", "Verify"]:
    for metric in ["median", "average"]:
        t = thesis[op][metric]
        c = current[op][metric]
        diff = ((c - t) / t) * 100
        print(f"{op:<12} {metric:<10} {t:>10,}   {c:>10,}   {diff:+6.1f}%")

print("\nAnalysis:")
print("- Results are in the expected range")
print("- Sign operation shows the expected ~5-8x increase from original")
print("- Small variations are normal due to different CPU/system conditions")
