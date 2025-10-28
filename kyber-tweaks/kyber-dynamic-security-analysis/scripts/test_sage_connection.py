#!/usr/bin/env python3
"""
Test script to verify SageMath installation and lattice estimator
"""

import subprocess
import sys
import json
from pathlib import Path

def test_sage_installation():
    """Test if SageMath is installed and accessible"""
    try:
        result = subprocess.run(["sage", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ SageMath is installed:")
            print(f"  {result.stdout.strip()}")
            return True
        else:
            print("✗ SageMath not found")
            return False
    except FileNotFoundError:
        print("✗ SageMath not found in PATH")
        return False

def test_lattice_estimator():
    """Test if lattice estimator can be imported in sage"""
    test_script = """
import sys
sys.path.insert(0, "../estimator/lattice-estimator")
try:
    from estimator import *
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
"""
    
    try:
        result = subprocess.run(
            ["sage", "-c", test_script],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if "SUCCESS" in result.stdout:
            print("✓ Lattice estimator can be imported")
            return True
        else:
            print("✗ Failed to import lattice estimator:")
            print(f"  {result.stdout}")
            print(f"  {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error testing lattice estimator: {e}")
        return False

def test_simple_estimation():
    """Test a simple security estimation"""
    params = {
        "n": 256,
        "k": 2,
        "eta1": 3,
        "eta2": 2,
        "q": 3329,
        "du": 10,
        "dv": 4
    }
    
    # The sage script is in sage-scripts directory
    sage_script = Path("../sage-scripts/kyber_estimator.sage")
    
    if not sage_script.exists():
        print(f"✗ Sage script not found at {sage_script}")
        return False
    
    try:
        cmd = ["sage", str(sage_script), json.dumps(params)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                print("✓ Security estimation successful")
                if output.get('primal') and output['primal'].get('classical'):
                    print(f"  Primal classical security: {output['primal']['classical']} bits")
                if output.get('dual') and output['dual'].get('classical'):
                    print(f"  Dual classical security: {output['dual']['classical']} bits")
                return True
            except json.JSONDecodeError:
                print("✗ Failed to parse estimation output")
                print(f"  Output: {result.stdout}")
                if result.stderr:
                    print(f"  Error: {result.stderr}")
                return False
        else:
            print("✗ Security estimation failed")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error running estimation: {e}")
        return False

def main():
    print("Testing Dynamic Security Analysis Setup")
    print("="*50)
    
    tests = [
        ("SageMath Installation", test_sage_installation),
        ("Lattice Estimator Import", test_lattice_estimator),
        ("Security Estimation", test_simple_estimation)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed < len(tests):
        print("\nPlease fix the failing tests before running the full analysis")
        sys.exit(1)
    else:
        print("\nAll tests passed! You can now run the dynamic analysis.")

if __name__ == "__main__":
    main()