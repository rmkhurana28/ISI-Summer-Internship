#!/usr/bin/env python3
"""
Kyber Security Analysis for Different Parameter Sets
This script analyzes the security of Kyber with various (du, dv) and eta values
"""

import json
import sys
from tabulate import tabulate
import subprocess
import os

class KyberSecurityAnalyzer:
    def __init__(self):
        # Parameter configurations matching your thesis
        self.du_dv_configs = {
            "Kyber512": [
                {"du": 10, "dv": 4, "delta": "2^-161", "dims": "(800, 768)"},
                {"du": 11, "dv": 3, "delta": "2^-148", "dims": "(800, 800)"},
                {"du": 9, "dv": 5, "delta": "2^-98", "dims": "(800, 736)"}
            ],
            "Kyber768": [
                {"du": 10, "dv": 4, "delta": "2^-165", "dims": "(1184, 1088)"},
                {"du": 11, "dv": 3, "delta": "2^-151", "dims": "(1184, 1152)"},
                {"du": 9, "dv": 5, "delta": "2^-99", "dims": "(1184, 1024)"}
            ],
            "Kyber1024": [
                {"du": 11, "dv": 5, "delta": "2^-175", "dims": "(1568, 1568)"},
                {"du": 12, "dv": 4, "delta": "2^-183", "dims": "(1568, 1664)"},
                {"du": 10, "dv": 6, "delta": "2^-151", "dims": "(1568, 1472)"}
            ]
        }
        
        self.eta_configs = {
            "Kyber512": {"eta1": 5, "eta2": 3, "delta": "2^-85", "dims": "(800, 768)"},
            "Kyber768": {"eta1": 4, "eta2": 4, "delta": "2^-50", "dims": "(1184, 1088)"},
            "Kyber1024": {"eta1": 4, "eta2": 4, "delta": "2^-47", "dims": "(1568, 1568)"}
        }
        
        # Security estimates from your thesis
        self.security_estimates = {
            "Kyber512": {
                "10_4": {
                    "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
                    "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
                },
                "11_3": {
                    "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
                    "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
                },
                "9_5": {
                    "primal": {"d": 999, "b": 406, "m": 486, "classical": 118, "quantum": 107},
                    "dual": {"d": 1024, "b": 403, "m": 512, "classical": 117, "quantum": 106}
                },
                "eta_5_3": {
                    "primal": {"d": 1027, "b": 439, "m": 514, "classical": 128, "quantum": 116},
                    "dual": {"d": 1027, "b": 515, "m": 436, "classical": 127, "quantum": 115}
                }
            },
            "Kyber768": {
                "10_4": {
                    "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
                    "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
                },
                "11_3": {
                    "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
                    "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
                },
                "9_5": {
                    "primal": {"d": 1419, "b": 626, "m": 650, "classical": 183, "quantum": 166},
                    "dual": {"d": 1418, "b": 620, "m": 650, "classical": 181, "quantum": 164}
                },
                "eta_4_4": {
                    "primal": {"d": 1489, "b": 688, "m": 720, "classical": 201, "quantum": 182},
                    "dual": {"d": 1487, "b": 719, "m": 683, "classical": 199, "quantum": 181}
                }
            },
            "Kyber1024": {
                "11_5": {
                    "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
                    "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
                },
                "12_4": {
                    "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
                    "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
                },
                "10_6": {
                    "primal": {"d": 1885, "b": 878, "m": 860, "classical": 256, "quantum": 232},
                    "dual": {"d": 1862, "b": 868, "m": 838, "classical": 253, "quantum": 230}
                },
                "eta_4_4": {
                    "primal": {"d": 1936, "b": 961, "m": 911, "classical": 281, "quantum": 254},
                    "dual": {"d": 1930, "b": 953, "m": 906, "classical": 278, "quantum": 252}
                }
            }
        }

    def generate_parameter_code(self, variant, config_num):
        """Generate the parameter set code for testing"""
        codes = {
            "Kyber512": {
                1: "ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**10, 2**4, ke_ct=2)",
                2: "ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**11, 2**3, ke_ct=2)",
                3: "ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**9, 2**5, ke_ct=2)"
            },
            "Kyber768": {
                1: "ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**10, 2**4)",
                2: "ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**11, 2**3)",
                3: "ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**9, 2**5)"
            },
            "Kyber1024": {
                1: "ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**11, 2**5)",
                2: "ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**12, 2**4)",
                3: "ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**10, 2**6)"
            }
        }
        return codes.get(variant, {}).get(config_num, "")

    def create_table_dudv(self, variant):
        """Create security analysis table for du,dv variations"""
        configs = self.du_dv_configs[variant]
        table_data = []
        
        for config in configs:
            du, dv = config["du"], config["dv"]
            key = f"{du}_{dv}"
            estimates = self.security_estimates[variant].get(key, {})
            
            if estimates:
                # Primal attack row
                primal = estimates["primal"]
                table_data.append([
                    f"(du = {du}, dv = {dv}) {config['delta']} {config['dims']}",
                    "Primal Attack",
                    primal["d"],
                    primal["b"],
                    primal["m"],
                    primal["classical"],
                    primal["quantum"],
                    "",  # δ
                    ""   # C
                ])
                
                # Dual attack row
                dual = estimates["dual"]
                table_data.append([
                    "",
                    "Dual Attack",
                    dual["d"],
                    dual["b"],
                    dual["m"],
                    dual["classical"],
                    dual["quantum"],
                    "",  # δ
                    ""   # C
                ])
                
                # Empty row for spacing
                table_data.append([""] * 9)
        
        headers = ["", "", "d", "b", "m", "Core-SVP\n(classical)", "Core-SVP\n(quantum)", "δ", "C"]
        return tabulate(table_data, headers=headers, tablefmt="grid")

    def create_table_eta(self):
        """Create security analysis table for eta variations"""
        table_data = []
        
        for variant, config in self.eta_configs.items():
            eta1, eta2 = config["eta1"], config["eta2"]
            key = f"eta_{eta1}_{eta2}"
            estimates = self.security_estimates[variant].get(key, {})
            
            if estimates:
                # Primal attack row
                primal = estimates["primal"]
                table_data.append([
                    f"{variant}\n(η1 = {eta1}, η2 = {eta2}) {config['delta']} {config['dims']}",
                    "Primal Attack",
                    primal["d"],
                    primal["b"],
                    primal["m"],
                    primal["classical"],
                    primal["quantum"],
                    "",  # δ
                    ""   # C
                ])
                
                # Dual attack row
                dual = estimates["dual"]
                table_data.append([
                    "",
                    "Dual Attack",
                    dual["d"],
                    dual["b"],
                    dual["m"],
                    dual["classical"],
                    dual["quantum"],
                    "",  # δ
                    ""   # C
                ])
                
                # Empty row for spacing
                table_data.append([""] * 9)
        
        headers = ["", "", "d", "b", "m", "Core-SVP\n(classical)", "Core-SVP\n(quantum)", "δ", "C"]
        return tabulate(table_data, headers=headers, tablefmt="grid")

    def generate_test_figures(self):
        """Generate test result figures (parameter sets)"""
        print("\n=== Test Result 5 ===")
        print("# Parameter sets")
        print("ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**10, 2**4, ke_ct=2)")
        print("ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**10, 2**4)")
        print("ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**11, 2**5)")
        
        print("\n=== Test Result 6 ===")
        print("# Parameter sets")
        print("ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**11, 2**3, ke_ct=2)")
        print("ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**11, 2**3)")
        print("ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**12, 2**4)")
        
        print("\n=== Test Result 7 ===")
        print("# Parameter sets")
        print("ps_light = KyberParameterSet(256, 2, 3, 2, 3329, 2**12, 2**9, 2**5, ke_ct=2)")
        print("ps_recommended = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**9, 2**5)")
        print("ps_paranoid = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**10, 2**6)")

    def run_analysis(self):
        """Run complete security analysis"""
        print("KYBER SECURITY ANALYSIS")
        print("=" * 80)
        
        # Generate test figures
        self.generate_test_figures()
        
        # Generate du,dv variation tables
        print("\n\n=== Table 5.5: Security analysis of Kyber512 with different du, dv values ===")
        print(self.create_table_dudv("Kyber512"))
        
        print("\n\n=== Table 5.6: Security analysis of Kyber768 with different du, dv values ===")
        print(self.create_table_dudv("Kyber768"))
        
        print("\n\n=== Table 5.7: Security analysis of Kyber1024 with different du, dv values ===")
        print(self.create_table_dudv("Kyber1024"))
        
        # Generate eta variation table
        print("\n\n=== Table 5.8: Security analysis of Kyber with different η1, η2 values ===")
        print(self.create_table_eta())

def main():
    analyzer = KyberSecurityAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()