#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "../api.h"
#include "../randombytes.h"

#define NTESTS 100
#define MLEN 32

// External functions for original implementation
int crypto_sign_keypair_original(unsigned char *pk, unsigned char *sk);
int crypto_sign_original(unsigned char *sm, size_t *smlen, 
                        const unsigned char *m, size_t mlen,
                        const unsigned char *sk);

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
    uint64_t cycles_tweaked = 0, cycles_original = 0;
    int i;
    
    printf("=== Dilithium Tweaks Performance Comparison ===\n\n");
    printf("Parameters:\n");
    printf("- Mode: %d\n", DILITHIUM_MODE);
    printf("- Tests: %d\n", NTESTS);
    printf("- Message length: %d bytes\n\n", MLEN);
    
    // Generate keypair
    printf("Generating keypair...\n");
    crypto_sign_keypair(pk, sk);
    
    // Generate random message
    randombytes(m, MLEN);
    
    printf("\nTesting Tweaked Implementation:\n");
    printf("- Tweak 1: SHA256 instead of SHAKE256\n");
    printf("- Tweak 2: Expanded coefficients {-2,-1,0,1,2}\n");
    printf("- Tweak 3: Relaxed rejection bounds (2*BETA)\n\n");
    
    // Warm up
    for(i = 0; i < 10; i++) {
        crypto_sign(sm, &smlen, m, MLEN, NULL, 0, sk);
    }
    
    // Measure tweaked version
    printf("Running %d signing operations (tweaked)...\n", NTESTS);
    start = rdtsc();
    for(i = 0; i < NTESTS; i++) {
        crypto_sign(sm, &smlen, m, MLEN, NULL, 0, sk);
    }
    end = rdtsc();
    cycles_tweaked = (end - start) / NTESTS;
    
    printf("Average cycles (tweaked): %lu\n", cycles_tweaked);
    printf("Average time (tweaked): %.3f ms\n\n", cycles_tweaked / 2800000.0);
    
    // Save results
    FILE *fp = fopen("test_results.txt", "w");
    if(fp) {
        fprintf(fp, "=== Test Results ===\n");
        fprintf(fp, "Tweaked implementation:\n");
        fprintf(fp, "  Average cycles: %lu\n", cycles_tweaked);
        fprintf(fp, "  Signature length: %zu\n", smlen);
        fclose(fp);
    }
    
    printf("Results saved to test_results.txt\n");
    
    return 0;
}