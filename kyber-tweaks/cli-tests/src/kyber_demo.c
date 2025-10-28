#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "params.h"
#include "kem.h"
#include "utils.h"

void print_banner(void) {
    printf("\n");
    printf("╔═══════════════════════════════════════════╗\n");
    printf("║     Kyber Parameter Tweaks Demo          ║\n");
    printf("║     Variant: Kyber%d                    ║\n", KYBER_K * 256);
    printf("╚═══════════════════════════════════════════╝\n");
    printf("\n");
}

void demo_sizes(void) {
    printf("\n=== Size Comparison ===\n");
    printf("Current configuration:\n");
    
    // Determine compression parameters
    int du, dv;
    int poly_bytes = KYBER_POLYCOMPRESSEDBYTES;
    int vec_bytes_per_k = KYBER_POLYVECCOMPRESSEDBYTES / KYBER_K;
    
    // Estimate du from polynomial compression
    switch(poly_bytes) {
        case 96:  du = 3; break;
        case 128: du = 4; break;
        case 160: du = 5; break;
        case 192: du = 6; break;
        default: du = -1;
    }
    
    // Estimate dv from polyvec compression
    switch(vec_bytes_per_k) {
        case 288: dv = 9; break;
        case 320: dv = 10; break;
        case 352: dv = 11; break;
        case 384: dv = 12; break;
        default: dv = -1;
    }
    
    printf("  Compression (du, dv): (%d, %d)\n", du, dv);
    printf("  eta1: %d, eta2: %d\n", KYBER_ETA1, KYBER_ETA2);
    printf("\nSize impact:\n");
    printf("  Public key:    %4d bytes\n", CRYPTO_PUBLICKEYBYTES);
    printf("  Secret key:    %4d bytes\n", CRYPTO_SECRETKEYBYTES);
    printf("  Ciphertext:    %4d bytes\n", CRYPTO_CIPHERTEXTBYTES);
    printf("  Shared secret: %4d bytes\n", CRYPTO_BYTES);
    
    // Show standard sizes for comparison
    int standard_ct_size = 0;
    if (KYBER_K == 2) standard_ct_size = 768;
    else if (KYBER_K == 3) standard_ct_size = 1088;
    else if (KYBER_K == 4) standard_ct_size = 1568;
    
    if (standard_ct_size > 0) {
        int diff = CRYPTO_CIPHERTEXTBYTES - standard_ct_size;
        float percent = (float)diff / standard_ct_size * 100;
        printf("\nCiphertext size vs standard: %+d bytes (%+.1f%%)\n", diff, percent);
    }
}

void demo_performance_estimate(void) {
    printf("\n=== Performance Characteristics ===\n");
    printf("Based on compression parameters:\n");
    
    int poly_bytes = KYBER_POLYCOMPRESSEDBYTES;
    
    // Estimate performance impact
    if (poly_bytes == 96) {
        printf("  • Compression (du=11, dv=3): ~50%% slower compression\n");
        printf("  • Overall impact: Minimal (~2-5%%)\n");
        printf("  • Trade-off: Good - saves space with low overhead\n");
    } else if (poly_bytes == 160 && KYBER_K == 2) {
        printf("  • Compression (du=9, dv=5): >100%% slower compression\n");
        printf("  • Overall impact: Moderate (~10-15%%)\n");
        printf("  • Trade-off: Use only if size critical\n");
    } else if (poly_bytes == 128 || poly_bytes == 160) {
        printf("  • Standard compression parameters\n");
        printf("  • Baseline performance\n");
    }
    
    if (KYBER_ETA1 > 3 || KYBER_ETA2 > 2) {
        printf("\nNoise parameter impact:\n");
        printf("  • Increased eta values detected\n");
        printf("  • Key generation: ~20-30%% slower\n");
        printf("  • Encryption: ~15-25%% slower\n");
    }
}

void run_demo(void) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss1[CRYPTO_BYTES];
    uint8_t ss2[CRYPTO_BYTES];
    clock_t start, end;
    double cpu_time_used;
    
    printf("\n=== Running Kyber Demo ===\n");
    
    // Key Generation
    printf("\n1. Generating keypair...\n");
    start = clock();
    crypto_kem_keypair(pk, sk);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC * 1000;
    printf("   ✓ Keypair generated in %.2f ms\n", cpu_time_used);
    
    // Encapsulation
    printf("\n2. Encapsulating (creating ciphertext)...\n");
    start = clock();
    crypto_kem_enc(ct, ss1, pk);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC * 1000;
    printf("   ✓ Ciphertext created in %.2f ms\n", cpu_time_used);
    printf("   Ciphertext size: %d bytes\n", CRYPTO_CIPHERTEXTBYTES);
    
    // Decapsulation
    printf("\n3. Decapsulating (recovering shared secret)...\n");
    start = clock();
    crypto_kem_dec(ss2, ct, sk);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC * 1000;
    printf("   ✓ Shared secret recovered in %.2f ms\n", cpu_time_used);
    
    // Verify
    printf("\n4. Verifying shared secrets match...\n");
    int match = (memcmp(ss1, ss2, CRYPTO_BYTES) == 0);
    if (match) {
        printf("   ✓ SUCCESS: Shared secrets match!\n");
        printf("   Shared secret (first 16 bytes): ");
        print_hex(ss1, 16);
    } else {
        printf("   ✗ ERROR: Shared secrets don't match!\n");
    }
    
    // Show sample data
    printf("\n5. Sample data visualization:\n");
    printf("   Public key (first 32 bytes):\n   ");
    print_hex(pk, 32);
    printf("   Ciphertext (first 32 bytes):\n   ");
    print_hex(ct, 32);
}

int main(int argc, char *argv[]) {
    int interactive = 1;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0) {
            printf("Kyber Parameter Demo\n");
            printf("Usage: %s [options]\n", argv[0]);
            printf("  -q    Quick mode (non-interactive)\n");
            printf("  -h    Show this help\n");
            return 0;
        } else if (strcmp(argv[i], "-q") == 0) {
            interactive = 0;
        }
    }
    
    print_banner();
    print_parameters();
    demo_sizes();
    demo_performance_estimate();
    
    if (interactive) {
        printf("\nPress Enter to run the demo...");
        getchar();
    }
    
    run_demo();
    
    printf("\n=== Demo Complete ===\n");
    printf("This configuration demonstrates ");
    
    // Identify configuration type
    if (KYBER_ETA1 > 3) {
        printf("modified noise parameters (eta variations)\n");
    } else if (KYBER_POLYCOMPRESSEDBYTES == 96) {
        printf("high compression (du=11, dv=3) with size reduction\n");
    } else if (KYBER_POLYCOMPRESSEDBYTES == 160 && KYBER_K == 2) {
        printf("extreme compression (du=9, dv=5) with significant overhead\n");
    } else {
        printf("standard Kyber parameters\n");
    }
    
    return 0;
}