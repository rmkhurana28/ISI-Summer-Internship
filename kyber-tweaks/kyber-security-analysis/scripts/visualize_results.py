#!/usr/bin/env python3
"""
Visualize Kyber security analysis results
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

def plot_security_comparison():
    """Create bar plots comparing security levels"""
    
    # Data from the tables
    kyber_variants = ['Kyber512', 'Kyber768', 'Kyber1024']
    
    # Classical security costs for different (du, dv) values
    dudv_configs = ['(10,4)', '(11,3)', '(9,5)']
    classical_costs = {
        'Kyber512': [118, 118, 118],
        'Kyber768': [183, 183, 183],
        'Kyber1024': [256, 256, 256]
    }
    
    quantum_costs = {
        'Kyber512': [107, 107, 107],
        'Kyber768': [166, 166, 166],
        'Kyber1024': [232, 232, 232]
    }
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Classical security plot
    x = np.arange(len(kyber_variants))
    width = 0.25
    
    for i, config in enumerate(dudv_configs):
        classical_values = [classical_costs[variant][i] for variant in kyber_variants]
        ax1.bar(x + i*width, classical_values, width, label=f'du,dv={config}')
    
    ax1.set_xlabel('Kyber Variant')
    ax1.set_ylabel('Core-SVP Classical Cost (log2)')
    ax1.set_title('Classical Security Analysis')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(kyber_variants)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Quantum security plot
    for i, config in enumerate(dudv_configs):
        quantum_values = [quantum_costs[variant][i] for variant in kyber_variants]
        ax2.bar(x + i*width, quantum_values, width, label=f'du,dv={config}')
    
    ax2.set_xlabel('Kyber Variant')
    ax2.set_ylabel('Core-SVP Quantum Cost (log2)')
    ax2.set_title('Quantum Security Analysis')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(kyber_variants)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('kyber_security_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_eta_comparison():
    """Create plots for eta variation analysis"""
    
    variants = ['Kyber512\n(η1=5,η2=3)', 'Kyber768\n(η1=4,η2=4)', 'Kyber1024\n(η1=4,η2=4)']
    primal_classical = [128, 201, 281]
    dual_classical = [127, 199, 278]
    primal_quantum = [116, 182, 254]
    dual_quantum = [115, 181, 252]
    
    x = np.arange(len(variants))
    width = 0.35
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Classical costs
    ax1.bar(x - width/2, primal_classical, width, label='Primal Attack', color='skyblue')
    ax1.bar(x + width/2, dual_classical, width, label='Dual Attack', color='lightcoral')
    ax1.set_xlabel('Kyber Variant')
    ax1.set_ylabel('Core-SVP Classical Cost (log2)')
    ax1.set_title('Classical Security with η Variations')
    ax1.set_xticks(x)
    ax1.set_xticklabels(variants)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Quantum costs
    ax2.bar(x - width/2, primal_quantum, width, label='Primal Attack', color='skyblue')
    ax2.bar(x + width/2, dual_quantum, width, label='Dual Attack', color='lightcoral')
    ax2.set_xlabel('Kyber Variant')
    ax2.set_ylabel('Core-SVP Quantum Cost (log2)')
    ax2.set_title('Quantum Security with η Variations')
    ax2.set_xticks(x)
    ax2.set_xticklabels(variants)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('kyber_eta_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("Generating security comparison plots...")
    plot_security_comparison()
    plot_eta_comparison()
    print("Plots saved as 'kyber_security_comparison.png' and 'kyber_eta_comparison.png'")

if __name__ == "__main__":
    main()