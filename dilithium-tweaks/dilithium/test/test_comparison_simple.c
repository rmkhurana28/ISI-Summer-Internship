#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include "../api.h"
#include "../sign.h"
#include "../randombytes.h"
#include "../params.h"

#define NTESTS 10
#define MLEN 32

// Function to measure cycles
static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

int main() {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t m[MLEN];
    uint8_t sm[MLEN + CRYPTO_BYTES];
    size_t smlen;
    uint64_t start, end;
    uint64_t cycles_total = 0;
    int i;
    
    printf("=== Dilithium Tweaks Test ===\n\n");
    printf("Parameters:\n");
    printf("- Mode: 3\n");
    printf("- Tests: %d\n", NTESTS);
    printf("- Message length: %d bytes\n\n", MLEN);
    
    // Generate keypair
    printf("Generating keypair...\n");
    if(crypto_sign_keypair(pk, sk) != 0) {
        printf("Keypair generation failed!\n");
        return 1;
    }
    
    // Generate random message
    randombytes(m, MLEN);
    
    printf("\nTesting Tweaked Implementation:\n");
    printf("- Tweak 1: SHA256 instead of SHAKE256\n");
    printf("- Tweak 2: Expanded coefficients {-2,-1,0,1,2}\n");
    printf("- Tweak 3: Relaxed rejection bounds (2*BETA)\n\n");
    
    // Test signing
    printf("Running %d signing operations...\n", NTESTS);
    for(i = 0; i < NTESTS; i++) {
        start = rdtsc();
        if(crypto_sign(sm, &smlen, m, MLEN, NULL, 0, sk) != 0) {
            printf("Signing failed!\n");
            return 1;
        }
        end = rdtsc();
        cycles_total += (end - start);
        printf("Test %d: Signature length = %zu\n", i+1, smlen);
    }
    
    printf("\nAverage cycles per signature: %lu\n", cycles_total / NTESTS);
    
    printf("\nTest completed successfully!\n");
    
    return 0;
}
