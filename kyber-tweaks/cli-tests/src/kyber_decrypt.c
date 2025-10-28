#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "params.h"
#include "kem.h"
#include "utils.h"

void print_usage(const char *program) {
    printf("Usage: %s [options] -s <secret_key_file> -c <ciphertext_file>\n", program);
    printf("Options:\n");
    printf("  -s <file>     Secret key file (required)\n");
    printf("  -c <file>     Ciphertext file (required)\n");
    printf("  -o <file>     Output file for shared secret (default: decrypted_secret.bin)\n");
    printf("  -f <format>   Output format: hex, base64, binary (default: binary)\n");
    printf("  -v            Verbose output\n");
    printf("  -p            Print parameters\n");
    printf("  -h            Show this help\n");
    printf("\nDecrypts Kyber ciphertext and outputs shared secret\n");
}

int main(int argc, char *argv[]) {
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];
    
    char *sk_file = NULL;
    char *ct_file = NULL;
    char *ss_file = "decrypted_secret.bin";
    char *format = "binary";
    int verbose = 0;
    int show_params = 0;
    size_t sk_len, ct_len;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-s") == 0 && i + 1 < argc) {
            sk_file = argv[++i];
        } else if (strcmp(argv[i], "-c") == 0 && i + 1 < argc) {
            ct_file = argv[++i];
        } else if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
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
    
    if (!sk_file || !ct_file) {
        fprintf(stderr, "Error: Both secret key and ciphertext files required\n");
        print_usage(argv[0]);
        return 1;
    }
    
    if (show_params) {
        print_parameters();
        print_sizes();
    }
    
    // Read secret key
    if (read_from_file(sk_file, sk, CRYPTO_SECRETKEYBYTES, &sk_len) != 0) {
        fprintf(stderr, "Error reading secret key from %s\n", sk_file);
        return 1;
    }
    
    if (sk_len != CRYPTO_SECRETKEYBYTES) {
        fprintf(stderr, "Error: Invalid secret key size. Expected %d, got %zu\n",
                CRYPTO_SECRETKEYBYTES, sk_len);
        return 1;
    }
    
    // Read ciphertext
    if (read_from_file(ct_file, ct, CRYPTO_CIPHERTEXTBYTES, &ct_len) != 0) {
        fprintf(stderr, "Error reading ciphertext from %s\n", ct_file);
        return 1;
    }
    
    if (ct_len != CRYPTO_CIPHERTEXTBYTES) {
        fprintf(stderr, "Error: Invalid ciphertext size. Expected %d, got %zu\n",
                CRYPTO_CIPHERTEXTBYTES, ct_len);
        return 1;
    }
    
    if (verbose) {
        printf("Secret key loaded from: %s (%zu bytes)\n", sk_file, sk_len);
        printf("Ciphertext loaded from: %s (%zu bytes)\n", ct_file, ct_len);
        printf("Performing Kyber%d decapsulation...\n", KYBER_K * 256);
    }
    
    // Perform decapsulation
    crypto_kem_dec(ss, ct, sk);
    
    // Output results
    if (strcmp(format, "binary") == 0) {
        // Save shared secret
        if (write_to_file(ss_file, ss, CRYPTO_BYTES) != 0) {
            return 1;
        }
        if (verbose) {
            printf("Shared secret saved to: %s (%d bytes)\n", 
                   ss_file, CRYPTO_BYTES);
        }
    } else if (strcmp(format, "hex") == 0) {
        printf("=== DECRYPTED SHARED SECRET ===\n");
        print_hex(ss, CRYPTO_BYTES);
    } else if (strcmp(format, "base64") == 0) {
        printf("=== DECRYPTED SHARED SECRET ===\n");
        print_base64(ss, CRYPTO_BYTES);
    }
    
    if (verbose) {
        printf("\nDecapsulation successful!\n");
        printf("Shared secret size: %d bytes\n", CRYPTO_BYTES);
    }
    
    return 0;
}