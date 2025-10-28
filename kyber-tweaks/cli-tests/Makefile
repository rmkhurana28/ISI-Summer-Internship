# Makefile for Kyber CLI Tests

CC = gcc
CFLAGS = -Wall -Wextra -O3 -fomit-frame-pointer -march=native
KYBER_DIR = ../kyber/ref
INCLUDES = -I$(KYBER_DIR) -I./src

# Kyber source files
KYBER_SOURCES = $(KYBER_DIR)/kem.c \
                $(KYBER_DIR)/indcpa.c \
                $(KYBER_DIR)/polyvec.c \
                $(KYBER_DIR)/poly.c \
                $(KYBER_DIR)/ntt.c \
                $(KYBER_DIR)/cbd.c \
                $(KYBER_DIR)/reduce.c \
                $(KYBER_DIR)/verify.c \
                $(KYBER_DIR)/symmetric-shake.c \
                $(KYBER_DIR)/sha256.c \
                $(KYBER_DIR)/sha512.c \
                $(KYBER_DIR)/fips202.c \
                $(KYBER_DIR)/randombytes.c

# CLI utilities
TARGETS = kyber_keygen kyber_encrypt kyber_decrypt kyber_demo

# Build all targets
all: $(TARGETS)

# Utility functions
src/utils.o: src/utils.c src/utils.h
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Key generation utility
kyber_keygen: src/kyber_keygen.c src/utils.o $(KYBER_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

# Encryption utility
kyber_encrypt: src/kyber_encrypt.c src/utils.o $(KYBER_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

# Decryption utility
kyber_decrypt: src/kyber_decrypt.c src/utils.o $(KYBER_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

# Interactive demo
kyber_demo: src/kyber_demo.c src/utils.o $(KYBER_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

# Build for specific Kyber variant
kyber512:
	$(MAKE) clean
	$(MAKE) all CFLAGS="$(CFLAGS) -DKYBER_K=2"

kyber768:
	$(MAKE) clean
	$(MAKE) all CFLAGS="$(CFLAGS) -DKYBER_K=3"

kyber1024:
	$(MAKE) clean
	$(MAKE) all CFLAGS="$(CFLAGS) -DKYBER_K=4"

clean:
	rm -f $(TARGETS) src/*.o

.PHONY: all clean kyber512 kyber768 kyber1024