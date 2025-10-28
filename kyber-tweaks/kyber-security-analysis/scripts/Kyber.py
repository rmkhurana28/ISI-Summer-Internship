#!/usr/bin/env python3
"""
Kyber.py - Individual parameter testing script for Kyber security analysis
This script outputs security analysis for specific parameter sets
"""

import sys
import argparse
from tabulate import tabulate

# Security estimates based on thesis tables (hardcoded data)
security_data = {
    # (du, dv) variations for Kyber512
    "512_10_4": {
        "d": "2^-161 (800, 768)",
        "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
        "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
    },
    "512_11_3": {
        "d": "2^-148 (800, 800)", 
        "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
        "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
    },
    "512_9_5": {
        "d": "2^-98 (800, 736)",
        "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
        "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
    },
    
    # (du, dv) variations for Kyber768
    "768_10_4": {
        "d": "2^-165 (1184, 1088)",
        "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
        "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
    },
    "768_11_3": {
        "d": "2^-151 (1184, 1152)",
        "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
        "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
    },
    "768_9_5": {
        "d": "2^-99 (1184, 1024)",
        "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
        "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
    },
    
    # (du, dv) variations for Kyber1024
    "1024_11_5": {
        "d": "2^-175 (1568, 1568)",
        "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
        "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
    },
    "1024_12_4": {
        "d": "2^-183 (1568, 1664)",
        "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
        "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
    },
    "1024_10_6": {
        "d": "2^-151 (1568, 1472)",
        "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
        "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
    },
    
    # Eta variations
    "512_eta_5_3": {
        "d": "2^-85 (800, 768)",
        "primal": {"d": 1027, "b": 439, "m": 514, "classical": 128, "quantum": 116},
        "dual": {"d": 1027, "b": 515, "m": 436, "classical": 127, "quantum": 115}
    },
    "768_eta_4_4": {
        "d": "2^-50 (1184, 1088)",
        "primal": {"d": 1489, "b": 688, "m": 720, "classical": 201, "quantum": 182},
        "dual": {"d": 1487, "b": 719, "m": 683, "classical": 199, "quantum": 181}
    },
    "1024_eta_4_4": {
        "d": "2^-47 (1568, 1568)",
        "primal": {"d": 1936, "b": 961, "m": 911, "classical": 281, "quantum": 254},
        "dual": {"d": 1930, "b": 953, "m": 906, "classical": 278, "quantum": 252}
    }
}

def print_parameter_set(param_set, du=None, dv=None):
    """Print the parameter set configuration"""
    if param_set == 512:
        variant = "ps_light"
        k = 2
        eta1 = 3
        eta2 = 2
    elif param_set == 768:
        variant = "ps_recommended"
        k = 3
        eta1 = 2
        eta2 = 2
    else:  # 1024
        variant = "ps_paranoid"
        k = 4
        eta1 = 2
        eta2 = 2
    
    print(f"\n# Parameter set for Kyber{param_set}")
    if du and dv:
        print(f"{variant} = KyberParameterSet(256, {k}, {eta1}, {eta2}, 3329, 2**12, 2**{du}, 2**{dv}", end="")
        if param_set == 512:
            print(", ke_ct=2)", end="")
        else:
            print(")", end="")
    print()

def print_table_format(param_set, du, dv, data):
    """Print results in thesis table format"""
    print(f"\nSecurity Analysis: Kyber{param_set} (du = {du}, dv = {dv})")
    print("=" * 100)
    
    headers = ["", "Attack Type", "d", "b", "m", "Core-SVP\n(classical)", "Core-SVP\n(quantum)", "δ", "C"]
    
    d_val = data['d']
    primal = data['primal']
    dual = data['dual']
    
    table_data = [
        [f"(du = {du}, dv = {dv}) {d_val}", "Primal Attack", primal['d'], primal['b'], 
         primal['m'], primal['classical'], primal['quantum'], "", ""],
        ["", "Dual Attack", dual['d'], dual['b'], 
         dual['m'], dual['classical'], dual['quantum'], "", ""]
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_eta_format(param_set, eta1, eta2, data):
    """Print results for eta variations"""
    print(f"\nSecurity Analysis: Kyber{param_set} (η1 = {eta1}, η2 = {eta2})")
    print("=" * 100)
    
    headers = ["", "Attack Type", "d", "b", "m", "Core-SVP\n(classical)", "Core-SVP\n(quantum)", "δ", "C"]
    
    d_val = data['d']
    primal = data['primal']
    dual = data['dual']
    
    table_data = [
        [f"(η1 = {eta1}, η2 = {eta2}) {d_val}", "Primal Attack", primal['d'], primal['b'], 
         primal['m'], primal['classical'], primal['quantum'], "", ""],
        ["", "Dual Attack", dual['d'], dual['b'], 
         dual['m'], dual['classical'], dual['quantum'], "", ""]
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(
        description='Kyber Security Analysis - Individual Parameter Testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test specific du,dv values:
  python3 Kyber.py --param-set 512 --du 10 --dv 4
  python3 Kyber.py --param-set 768 --du 11 --dv 3
  python3 Kyber.py --param-set 1024 --du 12 --dv 4
  
  # Test eta variations:
  python3 Kyber.py --param-set 512 --eta1 5 --eta2 3
  python3 Kyber.py --param-set 768 --eta1 4 --eta2 4
        """
    )
    
    parser.add_argument('--param-set', type=int, choices=[512, 768, 1024], required=True,
                        help='Kyber parameter set (512, 768, or 1024)')
    parser.add_argument('--du', type=int, help='du parameter value')
    parser.add_argument('--dv', type=int, help='dv parameter value')
    parser.add_argument('--eta1', type=int, help='eta1 parameter value')
    parser.add_argument('--eta2', type=int, help='eta2 parameter value')
    
    args = parser.parse_args()
    
    # Validate arguments
    if (args.du or args.dv) and (args.eta1 or args.eta2):
        parser.error("Cannot specify both (du,dv) and (eta1,eta2) parameters")
    
    if (args.du and not args.dv) or (args.dv and not args.du):
        parser.error("Both du and dv must be specified together")
    
    if (args.eta1 and not args.eta2) or (args.eta2 and not args.eta1):
        parser.error("Both eta1 and eta2 must be specified together")
    
    if not any([args.du, args.dv, args.eta1, args.eta2]):
        parser.error("Must specify either (du,dv) or (eta1,eta2) parameters")
    
    # Determine which data to use
    if args.eta1 and args.eta2:
        # Eta variation test
        if args.param_set == 512 and args.eta1 == 5 and args.eta2 == 3:
            key = "512_eta_5_3"
        elif args.param_set == 768 and args.eta1 == 4 and args.eta2 == 4:
            key = "768_eta_4_4"
        elif args.param_set == 1024 and args.eta1 == 4 and args.eta2 == 4:
            key = "1024_eta_4_4"
        else:
            print(f"Error: No data available for Kyber{args.param_set} with η1={args.eta1}, η2={args.eta2}")
            sys.exit(1)
    else:
        # du,dv variation test
        key = f"{args.param_set}_{args.du}_{args.dv}"
    
    # Check if data exists
    if key not in security_data:
        print(f"Error: No security data available for the specified parameters")
        print(f"Attempted key: {key}")
        sys.exit(1)
    
    # Get the data
    data = security_data[key]
    
    # Print parameter set configuration
    print_parameter_set(args.param_set, args.du, args.dv)
    
    # Print results
    if args.eta1:
        print_eta_format(args.param_set, args.eta1, args.eta2, data)
    else:
        print_table_format(args.param_set, args.du, args.dv, data)
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Parameter Set: Kyber{args.param_set}")
    if args.du:
        print(f"  Configuration: du={args.du}, dv={args.dv}")
    else:
        print(f"  Configuration: η1={args.eta1}, η2={args.eta2}")
    print(f"  Classical Security (Primal): {data['primal']['classical']} bits")
    print(f"  Quantum Security (Primal): {data['primal']['quantum']} bits")

if __name__ == "__main__":
    main()