#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "params.h" 
#include "api.h"     
#include "kem.h"     
#include "utils.h"

void print_usage(const char *program) {
    printf("Usage: %s [options]\n", program);
    printf("Options:\n");
    printf("  -o <prefix>   Output file prefix (default: kyber_key)\n");
    printf("  -f <format>   Output format: hex, base64, binary (default: binary)\n");
    printf("  -p            Print parameters and sizes\n");
    printf("  -v            Verbose output\n");
    printf("  -h            Show this help\n");
    printf("\nGenerates Kyber keypair and saves to files:\n");
    printf("  <prefix>.pub  - Public key\n");
    printf("  <prefix>.sec  - Secret key\n");
}

int main(int argc, char *argv[]) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    char *prefix = "kyber_key";
    char *format = "binary";
    int verbose = 0;
    int show_params = 0;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
            prefix = argv[++i];
        } else if (strcmp(argv[i], "-f") == 0 && i + 1 < argc) {
            format = argv[++i];
        } else if (strcmp(argv[i], "-v") == 0) {
            verbose = 1;
        } else if (strcmp(argv[i], "-p") == 0) {
            show_params = 1;
        } else if (strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            return 0;
        }
    }
    
    if (show_params) {
        print_parameters();
        print_sizes();
    }
    
    // Generate keypair
    if (verbose) {
        printf("Generating Kyber%d keypair...\n", KYBER_K * 256);
    }
    
    crypto_kem_keypair(pk, sk);
    
    // Save keys
    char filename[256];
    
    if (strcmp(format, "binary") == 0) {
        // Save public key
        snprintf(filename, sizeof(filename), "%s.pub", prefix);
        if (write_to_file(filename, pk, CRYPTO_PUBLICKEYBYTES) == 0) {
            if (verbose) printf("Public key saved to: %s\n", filename);
        } else {
            return 1;
        }
        
        // Save secret key
        snprintf(filename, sizeof(filename), "%s.sec", prefix);
        if (write_to_file(filename, sk, CRYPTO_SECRETKEYBYTES) == 0) {
            if (verbose) printf("Secret key saved to: %s\n", filename);
        } else {
            return 1;
        }
    } else if (strcmp(format, "hex") == 0) {
        printf("=== PUBLIC KEY ===\n");
        print_hex(pk, CRYPTO_PUBLICKEYBYTES);
        printf("\n=== SECRET KEY ===\n");
        print_hex(sk, CRYPTO_SECRETKEYBYTES);
    } else if (strcmp(format, "base64") == 0) {
        printf("=== PUBLIC KEY ===\n");
        print_base64(pk, CRYPTO_PUBLICKEYBYTES);
        printf("\n=== SECRET KEY ===\n");
        print_base64(sk, CRYPTO_SECRETKEYBYTES);
    }
    
    if (verbose && strcmp(format, "binary") == 0) {
        printf("\nKey generation successful!\n");
        printf("Public key: %d bytes\n", CRYPTO_PUBLICKEYBYTES);
        printf("Secret key: %d bytes\n", CRYPTO_SECRETKEYBYTES);
    }
    
    return 0;
}