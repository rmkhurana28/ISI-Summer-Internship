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

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Usage: %s <message_file> <signature_file> <public_key_file>\n", argv[0]);
        return 1;
    }
    
    // Read files
    uint8_t *message, *sig, *pk;
    size_t message_len, sig_len, pk_len;
    
    if (read_file(argv[1], &message, &message_len) != 0 ||
        read_file(argv[2], &sig, &sig_len) != 0 ||
        read_file(argv[3], &pk, &pk_len) != 0) {
        fprintf(stderr, "Error reading files\n");
        return 1;
    }
    
    // Verify
    int ret = pqcrystals_dilithium3_ref_verify(sig, sig_len,
                                               message, message_len,
                                               NULL, 0, pk);
    
    if (ret == 0) {
        printf("[✓] VALID SIGNATURE (using tweaked verifier)\n");
    } else {
        printf("[✗] INVALID SIGNATURE\n");
    }
    
    free(message);
    free(sig);
    free(pk);
    
    return ret;
}