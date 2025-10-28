#ifndef IMPLEMENTATIONS_H
#define IMPLEMENTATIONS_H

#include <stdint.h>
#include <stddef.h>
#include "common.h"

// Function pointers for different implementations
typedef struct {
    const char *name;
    const char *description;
    implementation_mode_t mode;
    
    // Keypair generation (same for all)
    int (*keypair)(uint8_t *pk, uint8_t *sk);
    
    // Signature generation (different for each)
    int (*sign)(uint8_t *sig, size_t *siglen, 
                const uint8_t *m, size_t mlen,
                const uint8_t *sk);
    
    // Verification (same for all)
    int (*verify)(const uint8_t *sig, size_t siglen,
                  const uint8_t *m, size_t mlen,
                  const uint8_t *pk);
                  
} implementation_t;

// Get implementation based on mode
implementation_t* get_implementation(implementation_mode_t mode);

// Get all implementations for comparison
void get_all_implementations(implementation_t **impls, int *count);

// Initialize implementations (must be called before use)
void init_implementations(void);

// Function declarations for the actual crypto functions
// These will be linked from the dilithium source files
int pqcrystals_dilithium3_ref_keypair(uint8_t *pk, uint8_t *sk);
int pqcrystals_dilithium3_ref_signature(uint8_t *sig, size_t *siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *ctx, size_t ctxlen,
                                        const uint8_t *sk);
int pqcrystals_dilithium3_ref_verify(const uint8_t *sig, size_t siglen,
                                     const uint8_t *m, size_t mlen,
                                     const uint8_t *ctx, size_t ctxlen,
                                     const uint8_t *pk);

// We'll define wrapper functions for the different sign implementations
int sign_baseline(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
int sign_tweaked(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
int sign_tweaked_prob(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
int verify_wrapper(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);

#endif