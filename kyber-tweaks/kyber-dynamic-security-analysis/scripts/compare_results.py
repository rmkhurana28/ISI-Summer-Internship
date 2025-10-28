#!/usr/bin/env python3
"""
Compare static (hardcoded) results with dynamic (calculated) results
"""

import json
import sys
from pathlib import Path
from tabulate import tabulate

# Import the static results from your previous analysis
STATIC_RESULTS = {
    "Kyber512": {
        "10_4": {"primal_classical": 118, "dual_classical": 117},
        "11_3": {"primal_classical": 118, "dual_classical": 117},
        "9_5": {"primal_classical": 118, "dual_classical": 117},
        "eta_5_3": {"primal_classical": 128, "dual_classical": 127}
    },
    "Kyber768": {
        "10_4": {"primal_classical": 183, "dual_classical": 181},
        "11_3": {"primal_classical": 183, "dual_classical": 181},
        "9_5": {"primal_classical": 183, "dual_classical": 181},
        "eta_4_4": {"primal_classical": 201, "dual_classical": 199}
    },
    "Kyber1024": {
        "11_5": {"primal_classical": 256, "dual_classical": 253},
        "12_4": {"primal_classical": 256, "dual_classical": 253},
        "10_6": {"primal_classical": 256, "dual_classical": 253},
        "eta_4_4": {"primal_classical": 281, "dual_classical": 278}
    }
}

def load_dynamic_results(results_file):
    """Load dynamic results from JSON file"""
    try:
        with open(results_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading dynamic results: {e}")
        return None

def compare_results(static, dynamic):
    """Compare static and dynamic results"""
    
    comparison_data = []
    
    for variant in [512, 768, 1024]:
        variant_key = f"Kyber{variant}"
        
        if f'kyber{variant}_dudv' in dynamic:
            for result in dynamic[f'kyber{variant}_dudv']:
                if not result or 'params' not in result:
                    continue
                
                params = result['params']
                du, dv = params['du'], params['dv']
                static_key = f"{du}_{dv}"
                
                if static_key in static.get(variant_key, {}):
                    static_val = static[variant_key][static_key]
                    
                    comparison_data.append([
                        f"Kyber{variant}",
                        f"du={du}, dv={dv}",
                        static_val['primal_classical'],
                        int(result.get('primal', {}).get('classical', 0)),
                        static_val['dual_classical'],
                        int(result.get('dual', {}).get('classical', 0))
                    ])
    
    headers = ["Variant", "Config", "Static Primal", "Dynamic Primal", "Static Dual", "Dynamic Dual"]
    print(tabulate(comparison_data, headers=headers, tablefmt="grid"))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compare_results.py <dynamic_results.json>")
        sys.exit(1)
    
    dynamic_results = load_dynamic_results(sys.argv[1])
    if dynamic_results:
        print("\nComparison of Static vs Dynamic Security Analysis")
        print("="*80)
        compare_results(STATIC_RESULTS, dynamic_results)

if __name__ == "__main__":
    main()