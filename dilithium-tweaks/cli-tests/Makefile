CC = gcc
CFLAGS = -Wall -O2 -DDILITHIUM_MODE=3
INCLUDES = -I. -I..
LDFLAGS = -lm -lssl -lcrypto

DILITHIUM_DIR = ../dilithium

# Common files (used by all implementations)
COMMON_SRCS = $(DILITHIUM_DIR)/packing.c \
              $(DILITHIUM_DIR)/polyvec.c \
              $(DILITHIUM_DIR)/ntt.c \
              $(DILITHIUM_DIR)/reduce.c \
              $(DILITHIUM_DIR)/rounding.c \
              $(DILITHIUM_DIR)/fips202.c \
              $(DILITHIUM_DIR)/symmetric-shake.c \
              $(DILITHIUM_DIR)/randombytes.c

# Our common files
CLI_COMMON = src/common.o

# Create separate object files for each implementation
OBJS_BASELINE = obj/sign_baseline.o obj/poly_baseline.o
OBJS_OPTION1 = obj/sign_option1.o obj/poly_option1.o  
OBJS_OPTION2 = obj/sign_option2.o obj/poly_option1.o

# All object files
ALL_IMPL_OBJS = $(OBJS_BASELINE) $(OBJS_OPTION1) $(OBJS_OPTION2)

# Common objects (compiled once)
COMMON_OBJS = $(patsubst %.c,obj/%.o,$(notdir $(COMMON_SRCS)))

# Targets
TARGETS = cli_keygen cli_sign cli_verify cli_compare

all: directories $(TARGETS)

directories:
	@mkdir -p obj output/keys output/signatures output/benchmarks output/reports

# Compile common Dilithium files
obj/%.o: $(DILITHIUM_DIR)/%.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Compile our common files
src/common.o: src/common.c include/common.h
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Compile baseline implementation
obj/sign_baseline.o: $(DILITHIUM_DIR)/sign.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

obj/poly_baseline.o: $(DILITHIUM_DIR)/poly.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Compile option1 implementation (relaxed bounds)
obj/sign_option1.o: $(DILITHIUM_DIR)/sign_tweaked.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

obj/poly_option1.o: $(DILITHIUM_DIR)/poly_tweaked.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Compile option2 implementation (probabilistic)
obj/sign_option2.o: $(DILITHIUM_DIR)/sign_tweaked_prob.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# For now, just use baseline implementation for keygen
cli_keygen: src/cli_keygen_simple.c $(CLI_COMMON) $(OBJS_BASELINE) $(COMMON_OBJS)
	$(CC) $(CFLAGS) $(INCLUDES) $^ $(LDFLAGS) -o $@

clean:
	rm -rf obj
	rm -f $(TARGETS) src/*.o
	rm -rf output/keys/* output/signatures/* output/benchmarks/* output/reports/*

.PHONY: all clean directories