#include "../include/implementations.h"
#include <string.h>

// Include Dilithium headers
#define DILITHIUM_MODE 3
#include "../dilithium/params.h"
#include "../dilithium/api.h"

// Function declarations for tweaked implementations
int crypto_sign_signature_tweaked(uint8_t *sig, size_t *siglen,
                                 const uint8_t *m, size_t mlen,
                                 const uint8_t *sk);
int crypto_sign_signature_tweaked_prob(uint8_t *sig, size_t *siglen,
                                      const uint8_t *m, size_t mlen,
                                      const uint8_t *sk);

// Wrapper for baseline signing
int sign_baseline(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk) {
    // Use empty context for standard signing
    return pqcrystals_dilithium3_ref_signature(sig, siglen, m, mlen, NULL, 0, sk);
}

// Wrapper for tweaked signing (option 1)
int sign_tweaked(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk) {
    return crypto_sign_signature_tweaked(sig, siglen, m, mlen, sk);
}

// Wrapper for tweaked probabilistic signing (option 2)
int sign_tweaked_prob(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk) {
    return crypto_sign_signature_tweaked_prob(sig, siglen, m, mlen, sk);
}

// Wrapper for verification
int verify_wrapper(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk) {
    // Use empty context for standard verification
    return pqcrystals_dilithium3_ref_verify(sig, siglen, m, mlen, NULL, 0, pk);
}

// Define the implementations
static implementation_t implementations[3] = {
    {
        .name = "baseline",
        .description = "Original Dilithium-3",
        .mode = MODE_BASELINE,
        .keypair = pqcrystals_dilithium3_ref_keypair,
        .sign = sign_baseline,
        .verify = verify_wrapper
    },
    {
        .name = "option1",
        .description = "Tweaks 1+2+3 with relaxed bounds (2×BETA)",
        .mode = MODE_OPTION1,
        .keypair = pqcrystals_dilithium3_ref_keypair,
        .sign = sign_tweaked,
        .verify = verify_wrapper
    },
    {
        .name = "option2",
        .description = "Tweaks 1+2+3 with probabilistic bypass (10%)",
        .mode = MODE_OPTION2,
        .keypair = pqcrystals_dilithium3_ref_keypair,
        .sign = sign_tweaked_prob,
        .verify = verify_wrapper
    }
};

// Get implementation by mode
implementation_t* get_implementation(implementation_mode_t mode) {
    if (mode >= 0 && mode < 3) {
        return &implementations[mode];
    }
    return NULL;
}

// Get all implementations
void get_all_implementations(implementation_t **impls, int *count) {
    *impls = implementations;
    *count = 3;
}

// Initialize implementations (placeholder for now)
void init_implementations(void) {
    // Nothing to do for now
}