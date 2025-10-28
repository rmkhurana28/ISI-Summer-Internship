#!/usr/bin/env sage
"""
Kyber security estimation using lattice-estimator
This script must be run with SageMath
"""

import sys
import json
from sage.all import *

# Add lattice estimator to path
sys.path.insert(0, "../estimator/lattice-estimator")

from estimator import *
from estimator.lwe_parameters import LWEParameters
from estimator.lwe_primal import primal_usvp
from estimator.lwe_dual import dual_hybrid
from estimator.nd import CenteredBinomial
from estimator.reduction import RC

def create_kyber_parameters(n, k, eta1, eta2, q, du, dv):
    """
    Create Kyber LWE parameters for security estimation
    
    Args:
        n: polynomial degree (256 for Kyber)
        k: module rank (2,3,4 for Kyber512/768/1024)
        eta1, eta2: noise parameters
        q: modulus (3329 for Kyber)
        du, dv: compression parameters
    """
    
    # Secret distribution (centered binomial with parameter eta1)
    Xs = CenteredBinomial(eta1)
    
    # Error distribution (centered binomial with parameter eta2)
    Xe = CenteredBinomial(eta2)
    
    # Create LWE parameters
    params = LWEParameters(
        n=n*k,          # dimension
        q=q,            # modulus
        Xs=Xs,          # secret distribution
        Xe=Xe,          # error distribution
        m=n*k,          # number of samples
        tag=f"kyber{k*256}"
    )
    
    return params

def estimate_security(params):
    """
    Estimate security using various attacks
    
    Returns dict with security estimates
    """
    results = {}
    
    # Primal attack
    try:
        primal_result = primal_usvp(params, red_cost_model=RC.BDGL16)
        results['primal'] = {
            'd': int(primal_result.get('d', 0)),
            'beta': int(primal_result.get('beta', 0)),
            'm': int(primal_result.get('m', 0)),
            'rop': float(primal_result.get('rop', 1)),
            'classical': int(log(primal_result.get('rop', 1), 2)),
            'quantum': int(log(primal_result.get('rop', 1), 2) * 0.5)
        }
    except Exception as e:
        print(f"Primal attack failed: {e}", file=sys.stderr)
        results['primal'] = None
    
    # Dual attack
    try:
        dual_result = dual_hybrid(params, red_cost_model=RC.BDGL16)
        results['dual'] = {
            'd': int(dual_result.get('d', 0)),
            'beta': int(dual_result.get('beta', 0)),
            'm': int(dual_result.get('m', 0)),
            'rop': float(dual_result.get('rop', 1)),
            'classical': int(log(dual_result.get('rop', 1), 2)),
            'quantum': int(log(dual_result.get('rop', 1), 2) * 0.5)
        }
    except Exception as e:
        print(f"Dual attack failed: {e}", file=sys.stderr)
        results['dual'] = None
    
    return results

def main():
    """Main function to process command line arguments and run estimation"""
    
    if len(sys.argv) < 2:
        print("Usage: sage kyber_estimator.sage '<json_params>'", file=sys.stderr)
        sys.exit(1)
    
    # Parse input parameters
    input_params = json.loads(sys.argv[1])
    
    n = input_params.get('n', 256)
    k = input_params.get('k')
    eta1 = input_params.get('eta1')
    eta2 = input_params.get('eta2')
    q = input_params.get('q', 3329)
    du = input_params.get('du')
    dv = input_params.get('dv')
    
    # Create Kyber parameters
    params = create_kyber_parameters(n, k, eta1, eta2, q, du, dv)
    
    # Estimate security
    results = estimate_security(params)
    
    # Add input parameters to results (ensure they are JSON serializable)
    results['params'] = {
        'n': int(n),
        'k': int(k),
        'eta1': int(eta1),
        'eta2': int(eta2),
        'q': int(q),
        'du': int(du),
        'dv': int(dv)
    }
    
    # Output results as JSON
    print(json.dumps(results))

if __name__ == "__main__":
    main()