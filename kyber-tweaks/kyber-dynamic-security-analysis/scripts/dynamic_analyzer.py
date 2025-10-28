#!/usr/bin/env python3
"""
Dynamic Kyber Security Analyzer
Interfaces with SageMath to compute actual security estimates
"""

import json
import subprocess
import os
import sys
from tabulate import tabulate
from pathlib import Path

class DynamicKyberAnalyzer:
    def __init__(self):
        self.sage_script = Path("../sage-scripts/kyber_estimator.sage")
        self.results_dir = Path("../results")
        
        # Kyber parameter configurations
        self.kyber_params = {
            512: {"n": 256, "k": 2, "eta1": 3, "eta2": 2, "q": 3329},
            768: {"n": 256, "k": 3, "eta1": 2, "eta2": 2, "q": 3329},
            1024: {"n": 256, "k": 4, "eta1": 2, "eta2": 2, "q": 3329}
        }
        
        # Test configurations
        self.test_configs = {
            "dudv_tests": {
                5: [{"du": 10, "dv": 4}, {"du": 11, "dv": 3}, {"du": 9, "dv": 5}],
                6: [{"du": 11, "dv": 3}, {"du": 12, "dv": 4}, {"du": 10, "dv": 6}],
                7: [{"du": 9, "dv": 5}, {"du": 10, "dv": 6}, {"du": 11, "dv": 5}]
            },
            "eta_tests": {
                512: {"eta1": 5, "eta2": 3},
                768: {"eta1": 4, "eta2": 4},
                1024: {"eta1": 4, "eta2": 4}
            }
        }
    
    def run_sage_estimator(self, params):
        """Run the SageMath estimator script"""
        try:
            # Convert params to JSON string
            params_json = json.dumps(params)
            
            # Run sage script
            cmd = ["sage", str(self.sage_script), params_json]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse output
            if result.stdout:
                return json.loads(result.stdout)
            else:
                print(f"Error: No output from sage script")
                print(f"Stderr: {result.stderr}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"Error running sage: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")
            print(f"Raw output: {result.stdout}")
            return None
    
    def analyze_parameter_set(self, variant, du, dv, custom_eta=None):
        """Analyze a specific parameter set"""
        
        # Get base parameters
        base_params = self.kyber_params[variant].copy()
        
        # Add compression parameters
        base_params['du'] = du
        base_params['dv'] = dv
        
        # Override eta if specified
        if custom_eta:
            base_params['eta1'] = custom_eta['eta1']
            base_params['eta2'] = custom_eta['eta2']
        
        print(f"\nAnalyzing Kyber{variant} with du={du}, dv={dv}", end="")
        if custom_eta:
            print(f", eta1={custom_eta['eta1']}, eta2={custom_eta['eta2']}")
        else:
            print()
        
        # Run security estimation
        results = self.run_sage_estimator(base_params)
        
        return results
    
    def format_results_table(self, results_list, table_type="dudv"):
        """Format results as a table matching thesis format"""
        
        headers = ["Config", "Attack", "d", "b", "m", "Core-SVP\n(classical)", "Core-SVP\n(quantum)", "δ", "C"]
        table_data = []
        
        for result in results_list:
            if not result or 'primal' not in result or 'dual' not in result:
                continue
                
            params = result['params']
            
            if table_type == "dudv":
                config_str = f"(du = {params['du']}, dv = {params['dv']})"
            else:
                config_str = f"Kyber{params['k']*256}\n(η1 = {params['eta1']}, η2 = {params['eta2']})"
            
            # Primal attack
            if result['primal']:
                primal = result['primal']
                table_data.append([
                    config_str,
                    "Primal Attack",
                    int(primal['d']),
                    int(primal['beta']),
                    int(primal['m']),
                    int(primal['classical']),
                    int(primal['quantum']),
                    "",  # δ
                    ""   # C
                ])
            
            # Dual attack
            if result['dual']:
                dual = result['dual']
                table_data.append([
                    "",
                    "Dual Attack",
                    int(dual['d']),
                    int(dual['beta']),
                    int(dual['m']),
                    int(dual['classical']),
                    int(dual['quantum']),
                    "",  # δ
                    ""   # C
                ])
            
            table_data.append([""] * 9)  # Empty row
        
        return tabulate(table_data, headers=headers, tablefmt="grid")
    
    def run_all_tests(self):
        """Run all security tests"""
        
        all_results = {}
        
        # Test each Kyber variant with different du,dv values
        for variant in [512, 768, 1024]:
            print(f"\n{'='*60}")
            print(f"Testing Kyber{variant}")
            print('='*60)
            
            variant_results = []
            
            # Standard du,dv tests
            for test_config in self.test_configs['dudv_tests'][5]:  # Using test 5 configs as example
                result = self.analyze_parameter_set(variant, test_config['du'], test_config['dv'])
                if result:
                    variant_results.append(result)
            
            all_results[f'kyber{variant}_dudv'] = variant_results
            
            # Eta variation test
            if variant in self.test_configs['eta_tests']:
                eta_config = self.test_configs['eta_tests'][variant]
                result = self.analyze_parameter_set(variant, 10, 4, custom_eta=eta_config)
                if result:
                    all_results[f'kyber{variant}_eta'] = [result]
        
        return all_results
    
    def generate_report(self):
        """Generate complete security analysis report"""
        
        print("\n" + "="*80)
        print("KYBER DYNAMIC SECURITY ANALYSIS REPORT")
        print("="*80)
        
        # Run all tests
        all_results = self.run_all_tests()
        
        # Generate tables for each variant
        for variant in [512, 768, 1024]:
            print(f"\n\nTable: Security analysis of Kyber{variant} with different du, dv values")
            print("-"*80)
            
            if f'kyber{variant}_dudv' in all_results:
                table = self.format_results_table(all_results[f'kyber{variant}_dudv'], table_type="dudv")
                print(table)
                
                # Save to file
                with open(self.results_dir / f"tables/kyber{variant}_dudv_analysis.txt", "w") as f:
                    f.write(f"Security analysis of Kyber{variant} with different du, dv values\n")
                    f.write("="*80 + "\n")
                    f.write(table)
        
        # Generate eta variation table
        print(f"\n\nTable: Security analysis of Kyber with different η1, η2 values")
        print("-"*80)
        
        eta_results = []
        for variant in [512, 768, 1024]:
            if f'kyber{variant}_eta' in all_results:
                eta_results.extend(all_results[f'kyber{variant}_eta'])
        
        if eta_results:
            table = self.format_results_table(eta_results, table_type="eta")
            print(table)
            
            # Save to file
            with open(self.results_dir / "tables/kyber_eta_analysis.txt", "w") as f:
                f.write("Security analysis of Kyber with different η1, η2 values\n")
                f.write("="*80 + "\n")
                f.write(table)
        
        # Save complete results as JSON
        with open(self.results_dir / "complete_results.json", "w") as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n\nResults saved to {self.results_dir}")

def main():
    analyzer = DynamicKyberAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main()