#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "api.h"
#include "params.h"
#include "kem.h" 
#include "utils.h"

void print_usage(const char *program) {
    printf("Usage: %s [options] -k <public_key_file>\n", program);
    printf("Options:\n");
    printf("  -k <file>     Public key file (required)\n");
    printf("  -o <file>     Output file for ciphertext (default: ciphertext.bin)\n");
    printf("  -s <file>     Output file for shared secret (default: shared_secret.bin)\n");
    printf("  -f <format>   Output format: hex, base64, binary (default: binary)\n");
    printf("  -v            Verbose output\n");
    printf("  -p            Print parameters\n");
    printf("  -h            Show this help\n");
    printf("\nEncrypts using Kyber KEM and outputs ciphertext and shared secret\n");
}

int main(int argc, char *argv[]) {
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];
    
    char *pk_file = NULL;
    char *ct_file = "ciphertext.bin";
    char *ss_file = "shared_secret.bin";
    char *format = "binary";
    int verbose = 0;
    int show_params = 0;
    size_t pk_len;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-k") == 0 && i + 1 < argc) {
            pk_file = argv[++i];
        } else if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
            ct_file = argv[++i];
        } else if (strcmp(argv[i], "-s") == 0 && i + 1 < argc) {
            ss_file = argv[++i];
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
    
    if (!pk_file) {
        fprintf(stderr, "Error: Public key file required\n");
        print_usage(argv[0]);
        return 1;
    }
    
    if (show_params) {
        print_parameters();
        print_sizes();
    }
    
    // Read public key
    if (read_from_file(pk_file, pk, CRYPTO_PUBLICKEYBYTES, &pk_len) != 0) {
        fprintf(stderr, "Error reading public key from %s\n", pk_file);
        return 1;
    }
    
    if (pk_len != CRYPTO_PUBLICKEYBYTES) {
        fprintf(stderr, "Error: Invalid public key size. Expected %d, got %zu\n",
                CRYPTO_PUBLICKEYBYTES, pk_len);
        return 1;
    }
    
    if (verbose) {
        printf("Public key loaded from: %s (%zu bytes)\n", pk_file, pk_len);
        printf("Performing Kyber%d encapsulation...\n", KYBER_K * 256);
    }
    
    // Perform encapsulation
    crypto_kem_enc(ct, ss, pk);
    
    // Output results
    if (strcmp(format, "binary") == 0) {
        // Save ciphertext
        if (write_to_file(ct_file, ct, CRYPTO_CIPHERTEXTBYTES) != 0) {
            return 1;
        }
        if (verbose) {
            printf("Ciphertext saved to: %s (%d bytes)\n", 
                   ct_file, CRYPTO_CIPHERTEXTBYTES);
        }
        
        // Save shared secret
        if (write_to_file(ss_file, ss, CRYPTO_BYTES) != 0) {
            return 1;
        }
        if (verbose) {
            printf("Shared secret saved to: %s (%d bytes)\n", 
                   ss_file, CRYPTO_BYTES);
        }
    } else if (strcmp(format, "hex") == 0) {
        printf("=== CIPHERTEXT ===\n");
        print_hex(ct, CRYPTO_CIPHERTEXTBYTES);
        printf("\n=== SHARED SECRET ===\n");
        print_hex(ss, CRYPTO_BYTES);
    } else if (strcmp(format, "base64") == 0) {
        printf("=== CIPHERTEXT ===\n");
        print_base64(ct, CRYPTO_CIPHERTEXTBYTES);
        printf("\n=== SHARED SECRET ===\n");
        print_base64(ss, CRYPTO_BYTES);
    }
    
    if (verbose) {
        printf("\nEncapsulation successful!\n");
        printf("Ciphertext size: %d bytes\n", CRYPTO_CIPHERTEXTBYTES);
        printf("Shared secret size: %d bytes\n", CRYPTO_BYTES);
    }
    
    return 0;
}