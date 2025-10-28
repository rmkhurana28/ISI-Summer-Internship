#ifndef UTILS_H
#define UTILS_H

#include <stdint.h>
#include <stdio.h>

// Display modes
#define DISPLAY_HEX 0
#define DISPLAY_BASE64 1

// File I/O helpers
int write_to_file(const char *filename, const uint8_t *data, size_t len);
int read_from_file(const char *filename, uint8_t *data, size_t max_len, size_t *actual_len);

// Display helpers
void print_hex(const uint8_t *data, size_t len);
void print_base64(const uint8_t *data, size_t len);
void print_parameters(void);

// Encoding/Decoding
void encode_base64(const uint8_t *input, size_t len, char *output);
int decode_base64(const char *input, uint8_t *output, size_t *out_len);

// Parameter info
const char* get_parameter_description(void);
void print_sizes(void);

#endif