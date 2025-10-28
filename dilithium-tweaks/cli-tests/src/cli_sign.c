#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include "../include/common.h"

// Include Dilithium headers
#define DILITHIUM_MODE 3
#include "../dilithium/params.h"
#include "../dilithium/api.h"

// Function declarations for all implementations
int pqcrystals_dilithium3_ref_signature(uint8_t *sig, size_t *siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *ctx, size_t ctxlen,
                                        const uint8_t *sk);

// Function pointers for different implementations
typedef int (*sign_func_t)(uint8_t *sig, size_t *siglen,
                          const uint8_t *m, size_t mlen,
                          const uint8_t *ctx, size_t ctxlen,
                          const uint8_t *sk);

// We'll use dynamic linking to select implementation at runtime
extern int sign_baseline(uint8_t *sig, size_t *siglen,
                        const uint8_t *m, size_t mlen,
                        const uint8_t *sk);
extern int sign_option1(uint8_t *sig, size_t *siglen,
                       const uint8_t *m, size_t mlen,
                       const uint8_t *sk);
extern int sign_option2(uint8_t *sig, size_t *siglen,
                       const uint8_t *m, size_t mlen,
                       const uint8_t *sk);

void print_usage(const char *prog) {
    printf("Usage: %s [options]\n", prog);
    printf("Options:\n");
    printf("  -i, --input <file>     Input message file\n");
    printf("  -k, --key <file>       Secret key file\n");
    printf("  -o, --output <file>    Output signature file\n");
    printf("  -m, --mode <mode>      Implementation mode (baseline|option1|option2)\n");
    printf("  -v, --verbose          Show signature details\n");
    printf("  -h, --help             Show this help message\n");
    printf("\n");
    printf("Modes:\n");
    printf("  baseline - Original Dilithium\n");
    printf("  option1  - Tweaks with relaxed bounds (slower)\n");
    printf("  option2  - Tweaks with probabilistic bypass\n");
    printf("\n");
    printf("Examples:\n");
    printf("  %s -i msg.txt -k key.sk -o sig.bin -m baseline\n", prog);
    printf("  %s -i msg.txt -k key.sk -o sig.bin -m option1 -v\n", prog);
}

int main(int argc, char *argv[]) {
    char *input_file = NULL;
    char *key_file = NULL;
    char *output_file = "signature.sig";
    implementation_mode_t mode = MODE_BASELINE;
    int verbose = 0;
    
    static struct option long_options[] = {
        {"input", required_argument, 0, 'i'},
        {"key", required_argument, 0, 'k'},
        {"output", required_argument, 0, 'o'},
        {"mode", required_argument, 0, 'm'},
        {"verbose", no_argument, 0, 'v'},
        {"help", no_argument, 0, 'h'},
        {0, 0, 0, 0}
    };
    
    int opt;
    while ((opt = getopt_long(argc, argv, "i:k:o:m:vh", long_options, NULL)) != -1) {
        switch (opt) {
            case 'i':
                input_file = optarg;
                break;
            case 'k':
                key_file = optarg;
                break;
            case 'o':
                output_file = optarg;
                break;
            case 'm':
                mode = parse_mode(optarg);
                if (mode == (implementation_mode_t)-1) {
                    fprintf(stderr, "Error: Invalid mode '%s'\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
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
    
    if (!input_file || !key_file) {
        fprintf(stderr, "Error: Input message and secret key are required\n");
        print_usage(argv[0]);
        return 1;
    }
    
    // Read message
    uint8_t *message;
    size_t message_len;
    if (read_file(input_file, &message, &message_len) != 0) {
        fprintf(stderr, "Error: Failed to read message file\n");
        return 1;
    }
    
    // Read secret key
    uint8_t *sk;
    size_t sk_len;
    if (read_file(key_file, &sk, &sk_len) != 0) {
        fprintf(stderr, "Error: Failed to read secret key file\n");
        free(message);
        return 1;
    }
    
    if (sk_len != CRYPTO_SECRETKEYBYTES) {
        fprintf(stderr, "Error: Invalid secret key size\n");
        free(message);
        free(sk);
        return 1;
    }
    
    // Allocate signature buffer
    uint8_t *sig = malloc(CRYPTO_BYTES);
    size_t siglen;
    
    printf("Signing message with %s implementation...\n", mode_to_string(mode));
    printf("Message file: %s (%zu bytes)\n", input_file, message_len);
    
    // For now, use baseline for all modes (we'll fix this later)
    double start_time = get_time_ms();
    int ret = pqcrystals_dilithium3_ref_signature(sig, &siglen, 
                                                  message, message_len,
                                                  NULL, 0, sk);
    double end_time = get_time_ms();
    
    if (ret != 0) {
        print_status("Signing failed", 0);
        free(message);
        free(sk);
        free(sig);
        return 1;
    }
    
    print_status("Signing successful", 1);
    printf("Time: %.2f ms\n", end_time - start_time);
    printf("Signature size: %zu bytes\n", siglen);
    
    // Construct output path
    char output_path[512];
    snprintf(output_path, sizeof(output_path), "output/signatures/%s", output_file);
    
    // Save signature
    if (write_file(output_path, sig, siglen) != 0) {
        fprintf(stderr, "Error: Failed to save signature\n");
        free(message);
        free(sk);
        free(sig);
        return 1;
    }
    
    printf("Signature saved to: %s\n", output_path);
    
    if (verbose) {
        printf("\nSignature (first 64 bytes):\n");
        print_hex(sig, siglen, 64);
    }
    
    free(message);
    free(sk);
    free(sig);
    
    return 0;
}