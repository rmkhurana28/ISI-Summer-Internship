#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/time.h>

// Color codes for terminal output
#define COLOR_RED     "\033[0;31m"
#define COLOR_GREEN   "\033[0;32m"
#define COLOR_YELLOW  "\033[0;33m"
#define COLOR_BLUE    "\033[0;34m"
#define COLOR_RESET   "\033[0m"

// Dilithium mode (we use mode 3)
#ifndef DILITHIUM_MODE
#define DILITHIUM_MODE 3
#endif

// File I/O functions
int read_file(const char *filename, uint8_t **data, size_t *len);
int write_file(const char *filename, const uint8_t *data, size_t len);

// Display functions
void print_hex(const uint8_t *data, size_t len, size_t max_bytes);
void print_status(const char *msg, int success);
void print_progress(const char *msg);

// Timing functions
double get_time_ms(void);
uint64_t get_cycles(void);

// Implementation modes for our tweaks
typedef enum {
    MODE_BASELINE = 0,
    MODE_OPTION1 = 1,   // Tweaks 1+2+3 with relaxed bounds
    MODE_OPTION2 = 2    // Tweaks 1+2+3 with probabilistic bypass
} implementation_mode_t;

// Convert mode to string
const char* mode_to_string(implementation_mode_t mode);

// Parse mode from string
implementation_mode_t parse_mode(const char *str);

#endif