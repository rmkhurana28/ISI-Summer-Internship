#include "../include/common.h"
#include <x86intrin.h>

int read_file(const char *filename, uint8_t **data, size_t *len) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        return -1;
    }
    
    fseek(f, 0, SEEK_END);
    *len = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    *data = malloc(*len);
    if (!*data) {
        fclose(f);
        return -1;
    }
    
    size_t read_len = fread(*data, 1, *len, f);
    fclose(f);
    
    if (read_len != *len) {
        free(*data);
        return -1;
    }
    
    return 0;
}

int write_file(const char *filename, const uint8_t *data, size_t len) {
    FILE *f = fopen(filename, "wb");
    if (!f) {
        return -1;
    }
    
    size_t written = fwrite(data, 1, len, f);
    fclose(f);
    
    return (written == len) ? 0 : -1;
}

void print_hex(const uint8_t *data, size_t len, size_t max_bytes) {
    size_t print_len = (max_bytes > 0 && len > max_bytes) ? max_bytes : len;
    
    for (size_t i = 0; i < print_len; i++) {
        printf("%02x", data[i]);
        if ((i + 1) % 32 == 0) {
            printf("\n");
        }
    }
    
    if (max_bytes > 0 && len > max_bytes) {
        printf("... (%zu more bytes)\n", len - max_bytes);
    } else if (print_len % 32 != 0) {
        printf("\n");
    }
}

void print_status(const char *msg, int success) {
    if (success) {
        printf("%s[✓]%s %s\n", COLOR_GREEN, COLOR_RESET, msg);
    } else {
        printf("%s[✗]%s %s\n", COLOR_RED, COLOR_RESET, msg);
    }
}

void print_progress(const char *msg) {
    printf("%s[*]%s %s\n", COLOR_BLUE, COLOR_RESET, msg);
}

double get_time_ms(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000.0 + tv.tv_usec / 1000.0;
}

uint64_t get_cycles(void) {
    return __rdtsc();
}

const char* mode_to_string(implementation_mode_t mode) {
    switch (mode) {
        case MODE_BASELINE:
            return "Baseline";
        case MODE_OPTION1:
            return "Option 1 (Relaxed Bounds)";
        case MODE_OPTION2:
            return "Option 2 (Probabilistic)";
        default:
            return "Unknown";
    }
}

implementation_mode_t parse_mode(const char *str) {
    if (strcmp(str, "baseline") == 0) {
        return MODE_BASELINE;
    } else if (strcmp(str, "option1") == 0) {
        return MODE_OPTION1;
    } else if (strcmp(str, "option2") == 0) {
        return MODE_OPTION2;
    }
    return -1;  // Invalid mode
}