#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include "../include/common.h"

// Include Dilithium headers
#define DILITHIUM_MODE 3
#include "../dilithium/params.h"
#include "../dilithium/api.h"

// Function declaration
int pqcrystals_dilithium3_ref_verify(const uint8_t *sig, size_t siglen,
                                     const uint8_t *m, size_t mlen,
                                     const uint8_t *ctx, size_t ctxlen,
                                     const uint8_t *pk);

void print_usage(const char *prog) {
    printf("Usage: %s [options]\n", prog);
    printf("Options:\n");
    printf("  -i, --input <file>     Input message file\n");
    printf("  -s, --sig <file>       Signature file\n");
    printf("  -k, --key <file>       Public key file\n");
    printf("  -v, --verbose          Show details\n");
    printf("  -h, --help             Show this help message\n");
    printf("\n");
    printf("Example:\n");
    printf("  %s -i msg.txt -s sig.bin -k key.pk\n", prog);
}

int main(int argc, char *argv[]) {
    char *input_file = NULL;
    char *sig_file = NULL;
    char *key_file = NULL;
    int verbose = 0;
    
    static struct option long_options[] = {
        {"input", required_argument, 0, 'i'},
        {"sig", required_argument, 0, 's'},
        {"key", required_argument, 0, 'k'},
        {"verbose", no_argument, 0, 'v'},
        {"help", no_argument, 0, 'h'},
        {0, 0, 0, 0}
    };
    
    int opt;
    while ((opt = getopt_long(argc, argv, "i:s:k:vh", long_options, NULL)) != -1) {
        switch (opt) {
            case 'i':
                input_file = optarg;
                break;
            case 's':
                sig_file = optarg;
                break;
            case 'k':
                key_file = optarg;
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
    
    if (!input_file || !sig_file || !key_file) {
        fprintf(stderr, "Error: Message, signature, and public key are required\n");
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
    
    // Read signature
    uint8_t *sig;
    size_t sig_len;
    if (read_file(sig_file, &sig, &sig_len) != 0) {
        fprintf(stderr, "Error: Failed to read signature file\n");
        free(message);
        return 1;
    }
    
    // Read public key
    uint8_t *pk;
    size_t pk_len;
    if (read_file(key_file, &pk, &pk_len) != 0) {
        fprintf(stderr, "Error: Failed to read public key file\n");
        free(message);
        free(sig);
        return 1;
    }
    
    if (pk_len != CRYPTO_PUBLICKEYBYTES) {
        fprintf(stderr, "Error: Invalid public key size\n");
        free(message);
        free(sig);
        free(pk);
        return 1;
    }
    
    printf("Verifying signature...\n");
    if (verbose) {
        printf("Message: %s (%zu bytes)\n", input_file, message_len);
        printf("Signature: %s (%zu bytes)\n", sig_file, sig_len);
        printf("Public key: %s (%zu bytes)\n", key_file, pk_len);
    }
    
    // Verify signature
    double start_time = get_time_ms();
    int ret = pqcrystals_dilithium3_ref_verify(sig, sig_len,
                                               message, message_len,
                                               NULL, 0, pk);
    double end_time = get_time_ms();
    
    if (ret == 0) {
        print_status("VALID SIGNATURE", 1);
    } else {
        print_status("INVALID SIGNATURE", 0);
    }
    printf("Verification time: %.2f ms\n", end_time - start_time);
    
    free(message);
    free(sig);
    free(pk);
    
    return (ret == 0) ? 0 : 1;
}