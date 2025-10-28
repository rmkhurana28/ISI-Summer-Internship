#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "../dilithium/api.h"
#include "../dilithium/sign.h"
#include "../dilithium/randombytes.h"

#define NTESTS 1000
#define MLEN 59

// Function to get CPU cycles
static inline uint64_t cpucycles(void) {
    unsigned int hi, lo;
    __asm__ __volatile__ ("rdtsc\n\t" : "=a" (lo), "=d" (hi));
    return ((uint64_t)lo) | (((uint64_t)hi) << 32);
}

// Comparison function for qsort
int compare_uint64(const void *a, const void *b) {
    uint64_t ua = *(const uint64_t*)a;
    uint64_t ub = *(const uint64_t*)b;
    return (ua > ub) - (ua < ub);
}

// Calculate median
uint64_t median(uint64_t *arr, int n) {
    qsort(arr, n, sizeof(uint64_t), compare_uint64);
    if (n % 2 == 0)
        return (arr[n/2-1] + arr[n/2]) / 2;
    else
        return arr[n/2];
}

// Calculate average
uint64_t average(uint64_t *arr, int n) {
    uint64_t sum = 0;
    for(int i = 0; i < n; i++)
        sum += arr[i];
    return sum / n;
}

int main() {
    unsigned char pk[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk[CRYPTO_SECRETKEYBYTES];
    unsigned char m[MLEN];
    unsigned char sm[MLEN + CRYPTO_BYTES];
    unsigned char m2[MLEN];
    size_t smlen, mlen;
    uint64_t tkeygen[NTESTS], tsign[NTESTS], tverify[NTESTS];
    uint64_t t_start, t_end;
    int i;
    
    printf("=== Dilithium Benchmark Results (Table 6.1 Format) ===\n");
    printf("Implementation: BASELINE\n");
    printf("- Tweak 1: SHA3-256 instead of SHAKE256\n");
    printf("- Tweak 2: Coefficients in {-2,-1,0,1,2}\n");
    printf("- Tweak 3: Relaxed rejection bounds (GAMMA - 2*BETA)\n");
    printf("Tests: %d runs\n\n", NTESTS);
    
    // Measure keypair generation
    printf("Measuring keypair generation...\n");
    for(i = 0; i < NTESTS; i++) {
        t_start = cpucycles();
        crypto_sign_keypair(pk, sk);
        t_end = cpucycles();
        tkeygen[i] = t_end - t_start;
    }
    
    // Measure signing
    printf("Measuring signing...\n");
    randombytes(m, MLEN);
    for(i = 0; i < NTESTS; i++) {
        t_start = cpucycles();
        crypto_sign(sm, &smlen, m, MLEN, NULL, 0, sk);
        t_end = cpucycles();
        tsign[i] = t_end - t_start;
    }
    
    // Measure verification
    printf("Measuring verification...\n");
    for(i = 0; i < NTESTS; i++) {
        t_start = cpucycles();
        crypto_sign_open(m2, &mlen, sm, smlen, NULL, 0, pk);
        t_end = cpucycles();
        tverify[i] = t_end - t_start;
    }
    
    // Calculate and display results in thesis format
    printf("\nResults (After Tweak):\n");
    printf("%-12s %-20s %-20s\n", "Operation", "Median (cycles)", "Average (cycles)");
    printf("%-12s %-20s %-20s\n", "---------", "---------------", "----------------");
    printf("%-12s %-20lu %-20lu\n", "Keypair", median(tkeygen, NTESTS), average(tkeygen, NTESTS));
    printf("%-12s %-20lu %-20lu\n", "Sign", median(tsign, NTESTS), average(tsign, NTESTS));
    printf("%-12s %-20lu %-20lu\n", "Verify", median(tverify, NTESTS), average(tverify, NTESTS));
    
    // Save results to file
    FILE *fp = fopen("results_tweaked_comprehensive.txt", "w");
    if(fp) {
        fprintf(fp, "Operation,Median,Average\n");
        fprintf(fp, "Keypair,%lu,%lu\n", median(tkeygen, NTESTS), average(tkeygen, NTESTS));
        fprintf(fp, "Sign,%lu,%lu\n", median(tsign, NTESTS), average(tsign, NTESTS));
        fprintf(fp, "Verify,%lu,%lu\n", median(tverify, NTESTS), average(tverify, NTESTS));
        fclose(fp);
    }
    
    return 0;
}
