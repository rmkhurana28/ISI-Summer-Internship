#include "utils.h"
#include "params.h"
#include "api.h" 
#include <string.h>
#include <stdlib.h>

static const char base64_chars[] = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

int write_to_file(const char *filename, const uint8_t *data, size_t len) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open file %s for writing\n", filename);
        return -1;
    }
    
    size_t written = fwrite(data, 1, len, fp);
    fclose(fp);
    
    if (written != len) {
        fprintf(stderr, "Error: Could not write all data to file\n");
        return -1;
    }
    
    return 0;
}

int read_from_file(const char *filename, uint8_t *data, size_t max_len, size_t *actual_len) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open file %s for reading\n", filename);
        return -1;
    }
    
    *actual_len = fread(data, 1, max_len, fp);
    fclose(fp);
    
    return 0;
}

void print_hex(const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", data[i]);
        if ((i + 1) % 32 == 0) printf("\n");
        else if ((i + 1) % 4 == 0) printf(" ");
    }
    if (len % 32 != 0) printf("\n");
}
void encode_base64(const uint8_t *input, size_t len, char *output) {
    size_t i, j;
    uint32_t val;
    
    for (i = 0, j = 0; i < len; i += 3, j += 4) {
        val = (i < len) ? input[i] << 16 : 0;
        val |= (i + 1 < len) ? input[i + 1] << 8 : 0;
        val |= (i + 2 < len) ? input[i + 2] : 0;
        
        output[j] = base64_chars[(val >> 18) & 0x3F];
        output[j + 1] = base64_chars[(val >> 12) & 0x3F];
        output[j + 2] = (i + 1 < len) ? base64_chars[(val >> 6) & 0x3F] : '=';
        output[j + 3] = (i + 2 < len) ? base64_chars[val & 0x3F] : '=';
    }
    output[j] = '\0';
}

void print_base64(const uint8_t *data, size_t len) {
    char *b64 = malloc((len * 4 / 3) + 4);
    if (!b64) return;
    
    encode_base64(data, len, b64);
    
    // Print in 64-char lines
    for (size_t i = 0; b64[i]; i += 64) {
        printf("%.64s\n", &b64[i]);
    }
    
    free(b64);
}

void print_parameters(void) {
    printf("=== Current Kyber Parameters ===\n");
    printf("Variant: Kyber%d\n", KYBER_K * 256);
    printf("Security Level: %d\n", KYBER_K);
    
#if KYBER_ETA1 == 2
    printf("eta1: 2 (standard)\n");
#elif KYBER_ETA1 == 3
    printf("eta1: 3 (standard for K=2)\n");
#elif KYBER_ETA1 == 4
    printf("eta1: 4 (modified)\n");
#elif KYBER_ETA1 == 5
    printf("eta1: 5 (modified)\n");
#endif

#if KYBER_ETA2 == 2
    printf("eta2: 2 (standard)\n");
#elif KYBER_ETA2 == 3
    printf("eta2: 3 (modified)\n");
#elif KYBER_ETA2 == 4
    printf("eta2: 4 (modified)\n");
#endif

    printf("==============================\n");
}

void print_sizes(void) {
    printf("\n=== Size Information ===\n");
    #ifdef CRYPTO_PUBLICKEYBYTES
        printf("Public Key: %d bytes\n", CRYPTO_PUBLICKEYBYTES);
    #else
        printf("Public Key: %d bytes\n", KYBER_PUBLICKEYBYTES);
    #endif
    
    #ifdef CRYPTO_SECRETKEYBYTES
        printf("Secret Key: %d bytes\n", CRYPTO_SECRETKEYBYTES);
    #else
        printf("Secret Key: %d bytes\n", KYBER_SECRETKEYBYTES);
    #endif
    
    #ifdef CRYPTO_CIPHERTEXTBYTES
        printf("Ciphertext: %d bytes\n", CRYPTO_CIPHERTEXTBYTES);
    #else
        printf("Ciphertext: %d bytes\n", KYBER_CIPHERTEXTBYTES);
    #endif
    
    #ifdef CRYPTO_BYTES
        printf("Shared Secret: %d bytes\n", CRYPTO_BYTES);
    #else
        printf("Shared Secret: %d bytes\n", KYBER_SSBYTES);
    #endif
    printf("=======================\n");
}

const char* get_parameter_description(void) {
    return "Current parameter set";
}