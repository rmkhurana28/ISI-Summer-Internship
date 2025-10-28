#!/usr/bin/env python3
"""
Check what's available in the lattice estimator
"""

import subprocess

# Test script to check available imports
test_script = '''
import sys
sys.path.insert(0, "../estimator/lattice-estimator")

print("Checking estimator.nd module...")
try:
    import estimator.nd as nd
    print("Available in estimator.nd:")
    for attr in dir(nd):
        if not attr.startswith('_'):
            print(f"  - {attr}")
except Exception as e:
    print(f"Error importing estimator.nd: {e}")

print("\\nChecking CenteredBinomial...")
try:
    from estimator.nd import CenteredBinomial
    print("✓ CenteredBinomial is available")
except Exception as e:
    print(f"✗ CenteredBinomial not available: {e}")

print("\\nChecking NoiseDistribution...")
try:
    from estimator.nd import NoiseDistribution
    print("✓ NoiseDistribution is available")
except Exception as e:
    print(f"✗ NoiseDistribution not available: {e}")
'''

# Run with sage
result = subprocess.run(["sage", "-c", test_script], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)