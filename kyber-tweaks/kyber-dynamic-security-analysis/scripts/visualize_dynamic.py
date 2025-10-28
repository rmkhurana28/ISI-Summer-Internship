#!/usr/bin/env python3
"""
Visualization for dynamic security analysis results
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_results(json_file):
    """Load results from JSON file"""
    with open(json_file, 'r') as f:
        return json.load(f)

def plot_security_comparison(results):
    """Create comparison plots for security levels"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    variants = [512, 768, 1024]
    primal_classical = []
    dual_classical = []
    primal_quantum = []
    dual_quantum = []
    
    for variant in variants:
        key = f'kyber{variant}_dudv'
        if key in results and results[key]:
            # Take the first result for simplicity
            result = results[key][0]
            if result and 'primal' in result and 'dual' in result:
                primal_classical.append(result['primal']['classical'])
                dual_classical.append(result['dual']['classical'])
                primal_quantum.append(result['primal']['quantum'])
                dual_quantum.append(result['dual']['quantum'])
            else:
                primal_classical.append(0)
                dual_classical.append(0)
                primal_quantum.append(0)
                dual_quantum.append(0)
    
    x = np.arange(len(variants))
    width = 0.35
    
    # Classical security
    ax1.bar(x - width/2, primal_classical, width, label='Primal Attack', color='skyblue')
    ax1.bar(x + width/2, dual_classical, width, label='Dual Attack', color='lightcoral')
    ax1.set_xlabel('Kyber Variant')
    ax1.set_ylabel('Security Level (bits)')
    ax1.set_title('Classical Security Analysis (Dynamic)')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'Kyber{v}' for v in variants])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Quantum security
    ax2.bar(x - width/2, primal_quantum, width, label='Primal Attack', color='skyblue')
    ax2.bar(x + width/2, dual_quantum, width, label='Dual Attack', color='lightcoral')
    ax2.set_xlabel('Kyber Variant')
    ax2.set_ylabel('Security Level (bits)')
    ax2.set_title('Quantum Security Analysis (Dynamic)')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'Kyber{v}' for v in variants])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/plots/dynamic_security_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved plot: dynamic_security_comparison.png")

def plot_dudv_variations(results):
    """Plot security levels for different du,dv configurations"""
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, variant in enumerate([512, 768, 1024]):
        ax = axes[idx]
        key = f'kyber{variant}_dudv'
        
        if key not in results or not results[key]:
            continue
        
        configs = []
        primal_vals = []
        dual_vals = []
        
        for result in results[key]:
            if result and 'params' in result:
                params = result['params']
                config_label = f"({params['du']},{params['dv']})"
                configs.append(config_label)
                
                if 'primal' in result and result['primal']:
                    primal_vals.append(result['primal']['classical'])
                else:
                    primal_vals.append(0)
                
                if 'dual' in result and result['dual']:
                    dual_vals.append(result['dual']['classical'])
                else:
                    dual_vals.append(0)
        
        x = np.arange(len(configs))
        width = 0.35
        
        ax.bar(x - width/2, primal_vals, width, label='Primal', color='skyblue')
        ax.bar(x + width/2, dual_vals, width, label='Dual', color='lightcoral')
        ax.set_xlabel('(du, dv) Configuration')
        ax.set_ylabel('Classical Security (bits)')
        ax.set_title(f'Kyber{variant} Security vs (du,dv)')
        ax.set_xticks(x)
        ax.set_xticklabels(configs)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../results/plots/dudv_variations.png', dpi=300, bbox_inches='tight')
    print("Saved plot: dudv_variations.png")

def main():
    """Generate all visualizations"""
    results_file = Path('../results/complete_results.json')
    
    if not results_file.exists():
        print(f"Results file not found: {results_file}")
        print("Please run dynamic_analyzer.py first")
        return
    
    results = load_results(results_file)
    
    print("Generating dynamic analysis visualizations...")
    plot_security_comparison(results)
    plot_dudv_variations(results)
    print("Visualization complete!")

if __name__ == "__main__":
    main()