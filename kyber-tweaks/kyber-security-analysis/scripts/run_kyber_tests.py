#!/usr/bin/env python3
"""
Script to run Kyber security tests for specific parameter sets
"""

import subprocess
import os
import sys

def run_parameter_test(test_number):
    """Run a specific parameter test configuration"""
    
    # Parameter configurations for each test
    test_configs = {
        5: {
            "kyber512": {"du": 10, "dv": 4},
            "kyber768": {"du": 10, "dv": 4},
            "kyber1024": {"du": 11, "dv": 5}
        },
        6: {
            "kyber512": {"du": 11, "dv": 3},
            "kyber768": {"du": 11, "dv": 3},
            "kyber1024": {"du": 12, "dv": 4}
        },
        7: {
            "kyber512": {"du": 9, "dv": 5},
            "kyber768": {"du": 9, "dv": 5},
            "kyber1024": {"du": 10, "dv": 6}
        }
    }
    
    if test_number not in test_configs:
        print(f"Invalid test number: {test_number}")
        return
    
    print(f"\n=== Running Test Result {test_number} ===")
    config = test_configs[test_number]
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kyber_py_path = os.path.join(script_dir, "Kyber.py")
    
    # Run for each Kyber variant
    for variant, params in config.items():
        param_set = int(variant.replace("kyber", ""))
        du = params["du"]
        dv = params["dv"]
        
        print(f"\nKyber{param_set} (du={du}, dv={dv}):")
        cmd = [sys.executable, kyber_py_path, "--param-set", str(param_set), "--du", str(du), "--dv", str(dv)]
        subprocess.run(cmd)

def run_eta_tests():
    """Run eta variation tests"""
    print("\n=== Running Eta Variation Tests ===")
    
    eta_configs = [
        {"param_set": 512, "eta1": 5, "eta2": 3},
        {"param_set": 768, "eta1": 4, "eta2": 4},
        {"param_set": 1024, "eta1": 4, "eta2": 4}
    ]
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kyber_py_path = os.path.join(script_dir, "Kyber.py")
    
    for config in eta_configs:
        print(f"\nKyber{config['param_set']} (η1={config['eta1']}, η2={config['eta2']}):")
        cmd = [sys.executable, kyber_py_path, 
               "--param-set", str(config['param_set']), 
               "--eta1", str(config['eta1']), 
               "--eta2", str(config['eta2'])]
        subprocess.run(cmd)

def main():
    # Run all parameter tests
    for test_num in [5, 6, 7]:
        run_parameter_test(test_num)
    
    # Run eta variation tests
    run_eta_tests()

if __name__ == "__main__":
    main()