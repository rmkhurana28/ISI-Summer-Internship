#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include "../include/common.h"
#include "../include/implementations.h"

// Include Dilithium parameters
#define DILITHIUM_MODE 3
#include "../dilithium/params.h"

void print_usage(const char *prog) {
    printf("Usage: %s [options]\n", prog);
    printf("Options:\n");
    printf("  -o, --output <name>    Output file prefix (default: key)\n");
    printf("  -v, --verbose          Show key details\n");
    printf("  -h, --help             Show this help message\n");
    printf("\n");
    printf("Examples:\n");
    printf("  %s -o mykey                # Generate mykey.pk and mykey.sk\n", prog);
    printf("  %s -o test -v             # Generate with verbose output\n", prog);
}

int main(int argc, char *argv[]) {
    char *output_prefix = "key";
    int verbose = 0;
    
    // Parse command line options
    static struct option long_options[] = {
        {"output", required_argument, 0, 'o'},
        {"verbose", no_argument, 0, 'v'},
        {"help", no_argument, 0, 'h'},
        {0, 0, 0, 0}
    };
    
    int opt;
    while ((opt = getopt_long(argc, argv, "o:vh", long_options, NULL)) != -1) {
        switch (opt) {
            case 'o':
                output_prefix = optarg;
                break;
            case 'v':
                verbose = 1;
                break;
            case 'h':
                print_usage(argv[0]);
                return 0;
            default:
                print_usage(argv[0]);
                return 1;
        }
    }
    
    // Allocate memory for keys
    uint8_t *pk = malloc(CRYPTO_PUBLICKEYBYTES);
    uint8_t *sk = malloc(CRYPTO_SECRETKEYBYTES);
    
    if (!pk || !sk) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        return 1;
    }
    
    // Initialize implementations
    init_implementations();
    
    // Get any implementation (they all use the same keypair function)
    implementation_t *impl = get_implementation(MODE_BASELINE);
    if (!impl) {
        fprintf(stderr, "Error: Failed to get implementation\n");
        free(pk);
        free(sk);
        return 1;
    }
    
    print_progress("Generating Dilithium-3 key pair...");
    
    // Generate key pair
    double start_time = get_time_ms();
    int ret = impl->keypair(pk, sk);
    double end_time = get_time_ms();
    
    if (ret != 0) {
        print_status("Key generation failed", 0);
        free(pk);
        free(sk);
        return 1;
    }
    
    print_status("Key generation successful", 1);
    printf("Time: %.2f ms\n\n", end_time - start_time);
    
    // Create output filenames
    char pk_filename[256], sk_filename[256];
    snprintf(pk_filename, sizeof(pk_filename), "output/keys/%s.pk", output_prefix);
    snprintf(sk_filename, sizeof(sk_filename), "output/keys/%s.sk", output_prefix);
    
    // Save keys
    if (write_file(pk_filename, pk, CRYPTO_PUBLICKEYBYTES) != 0) {
        fprintf(stderr, "Error: Failed to write public key\n");
        free(pk);
        free(sk);
        return 1;
    }
    
    if (write_file(sk_filename, sk, CRYPTO_SECRETKEYBYTES) != 0) {
        fprintf(stderr, "Error: Failed to write secret key\n");
        free(pk);
        free(sk);
        return 1;
    }
    
    printf("Keys saved:\n");
    printf("  Public key:  %s (%d bytes)\n", pk_filename, CRYPTO_PUBLICKEYBYTES);
    printf("  Secret key:  %s (%d bytes)\n", sk_filename, CRYPTO_SECRETKEYBYTES);
    
    if (verbose) {
        printf("\nPublic key (first 64 bytes):\n");
        print_hex(pk, CRYPTO_PUBLICKEYBYTES, 64);
        printf("\nSecret key (first 64 bytes):\n");
        print_hex(sk, CRYPTO_SECRETKEYBYTES, 64);
    }
    
    free(pk);
    free(sk);
    
    return 0;
}