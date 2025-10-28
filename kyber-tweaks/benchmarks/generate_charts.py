#!/usr/bin/env python3
"""
Generate performance comparison charts for Kyber benchmarks
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def load_analysis_data(json_file):
    """Load analysis data from JSON file"""
    with open(json_file, 'r') as f:
        return json.load(f)

def create_compression_comparison_chart(data, output_dir):
    """Create bar chart comparing compression operations"""
    
    # Setup the figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Compression Operation Performance Impact', fontsize=16)
    
    variants = ['kyber512', 'kyber768', 'kyber1024']
    compression_tests = {
        'test1_compression_du10_dv4': '(10,4)',
        'test2_compression_du11_dv3': '(11,3)',
        'test3_compression_du9_dv5': '(9,5)'
    }
    
    baseline_test = 'baseline_standard'
    
    for idx, variant in enumerate(variants):
        ax = axes[idx]
        ax.set_title(f'{variant.upper()}')
        
        # Get baseline value
        baseline_compress = data['tests'][baseline_test]['results'][variant]['poly_compress']['median']
        
        # Prepare data for plotting
        labels = ['Baseline']
        values = [baseline_compress]
        
        for test_name, test_label in compression_tests.items():
            if test_name in data['tests']:
                test_data = data['tests'][test_name]['results'].get(variant, {})
                if 'poly_compress' in test_data:
                    labels.append(test_label)
                    values.append(test_data['poly_compress']['median'])
        
        # Create bars
        x = np.arange(len(labels))
        bars = ax.bar(x, values)
        
        # Color baseline differently
        bars[0].set_color('gray')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        ax.set_xlabel('(du, dv) Configuration')
        ax.set_ylabel('Cycles')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'compression_comparison.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved compression comparison chart to: {output_file}")
    plt.close()

def create_eta_impact_chart(data, output_dir):
    """Create chart showing eta parameter impact"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Impact of η Parameter Variations', fontsize=16)
    
    variants = ['kyber512', 'kyber768', 'kyber1024']
    baseline_test = 'baseline_standard'
    eta_test = 'test4_eta_variations'
    
    # Chart 1: Noise generation time
    ax1.set_title('Noise Generation Time (Tη1)')
    
    baseline_values = []
    modified_values = []
    
    for variant in variants:
        baseline_eta1 = data['tests'][baseline_test]['results'][variant].get('poly_getnoise_eta1', {}).get('median', 0)
        modified_eta1 = data['tests'][eta_test]['results'][variant].get('poly_getnoise_eta1', {}).get('median', 0)
        
        baseline_values.append(baseline_eta1)
        modified_values.append(modified_eta1)
    
    x = np.arange(len(variants))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, baseline_values, width, label='Baseline η')
    bars2 = ax1.bar(x + width/2, modified_values, width, label='Modified η')
    
    ax1.set_xlabel('Kyber Variant')
    ax1.set_ylabel('Cycles')
    ax1.set_xticks(x)
    ax1.set_xticklabels([v.upper() for v in variants])
    ax1.legend()
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
    
    # Chart 2: Impact on KeyGen and Enc
    ax2.set_title('Impact on Key Generation and Encryption')
    
    metrics = ['indcpa_keypair', 'indcpa_enc']
    metric_labels = ['KeyGen', 'Enc']
    
    # Calculate percentage changes
    changes = {variant: {} for variant in variants}
    
    for variant in variants:
        for metric in metrics:
            baseline_val = data['tests'][baseline_test]['results'][variant][metric]['median']
            modified_val = data['tests'][eta_test]['results'][variant][metric]['median']
            change_pct = ((modified_val - baseline_val) / baseline_val) * 100
            changes[variant][metric] = change_pct
    
    # Plot grouped bars
    x = np.arange(len(variants))
    width = 0.35
    
    keygen_changes = [changes[v]['indcpa_keypair'] for v in variants]
    enc_changes = [changes[v]['indcpa_enc'] for v in variants]
    
    bars1 = ax2.bar(x - width/2, keygen_changes, width, label='KeyGen')
    bars2 = ax2.bar(x + width/2, enc_changes, width, label='Enc')
    
    ax2.set_xlabel('Kyber Variant')
    ax2.set_ylabel('Change from Baseline (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels([v.upper() for v in variants])
    ax2.legend()
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'eta_impact.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved eta impact chart to: {output_file}")
    plt.close()

def create_performance_summary_chart(data, output_dir):
    """Create overall performance summary chart"""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('Overall Performance Impact Summary', fontsize=16)
    
    # Focus on main operations
    operations = ['indcpa_keypair', 'indcpa_enc', 'indcpa_dec']
    op_labels = ['Key Generation', 'Encryption', 'Decryption']
    
    test_configs = {
        'test2_compression_du11_dv3': 'Compression\n(11,3)',
        'test3_compression_du9_dv5': 'Compression\n(9,5)',
        'test4_eta_variations': 'Eta\nVariations'
    }
    
    baseline_test = 'baseline_standard'
    
    # Prepare data - calculate average impact across all variants
    test_impacts = {}
    
    for test_name, test_label in test_configs.items():
        if test_name not in data['tests']:
            continue
            
        impacts = []
        
        for variant in ['kyber512', 'kyber768', 'kyber1024']:
            if variant not in data['tests'][test_name]['results']:
                continue
                
            for op in operations:
                baseline_val = data['tests'][baseline_test]['results'][variant][op]['median']
                test_val = data['tests'][test_name]['results'][variant][op]['median']
                change_pct = ((test_val - baseline_val) / baseline_val) * 100
                impacts.append(change_pct)
        
        if impacts:
            test_impacts[test_label] = {
                'avg': np.mean(impacts),
                'std': np.std(impacts),
                'min': np.min(impacts),
                'max': np.max(impacts)
            }
    
    # Create bar chart with error bars
    labels = list(test_impacts.keys())
    averages = [test_impacts[l]['avg'] for l in labels]
    errors = [test_impacts[l]['std'] for l in labels]
    
    x = np.arange(len(labels))
    bars = ax.bar(x, averages, yerr=errors, capsize=10)
    
    # Color bars based on positive/negative
    for bar, avg in zip(bars, averages):
        if avg > 0:
            bar.set_color('salmon')
        else:
            bar.set_color('lightgreen')
    
    ax.set_xlabel('Parameter Configuration')
    ax.set_ylabel('Average Performance Impact (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    # Add value labels
    for bar, avg, err in zip(bars, averages, errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{avg:.1f}%\n±{err:.1f}', ha='center', 
                va='bottom' if height > 0 else 'top')
    
    # Add text box with details
    textstr = 'Average impact across:\n• 3 Kyber variants\n• 3 main operations\n  (KeyGen, Enc, Dec)'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'performance_summary.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved performance summary chart to: {output_file}")
    plt.close()

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # Find most recent analysis
        results_dir = "./results"
        runs = sorted([d for d in os.listdir(results_dir) if d.startswith('run_')])
        if not runs:
            print("No benchmark runs found!")
            sys.exit(1)
        
        latest_run = runs[-1]
        json_file = os.path.join(results_dir, latest_run, 'analysis_data.json')
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found!")
        sys.exit(1)
    
    print(f"Loading data from: {json_file}")
    data = load_analysis_data(json_file)
    
    # Output directory for charts
    output_dir = os.path.dirname(json_file)
    
    # Generate charts
    create_compression_comparison_chart(data, output_dir)
    create_eta_impact_chart(data, output_dir)
    create_performance_summary_chart(data, output_dir)
    
    print(f"\nAll charts saved to: {output_dir}")

if __name__ == "__main__":
    main()