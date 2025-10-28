CC = gcc
CFLAGS = -Wall -O3 -fomit-frame-pointer
LDFLAGS = -lssl -lcrypto

all: benchmark_original benchmark_tweaked

benchmark_original: benchmark_sign.c
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=3 -I../ -o $@ $< \
	../sign.c ../packing.c ../polyvec.c ../poly.c ../ntt.c ../reduce.c \
	../rounding.c ../fips202.c ../symmetric-shake.c ../randombytes.c $(LDFLAGS)

benchmark_tweaked: benchmark_sign.c
	$(CC) $(CFLAGS) -DDILITHIUM_MODE=3 -I../ -o $@ $< \
	../sign_tweaked.c ../packing.c ../polyvec.c ../poly_tweaked.c ../ntt.c ../reduce.c \
	../rounding.c ../fips202.c ../symmetric-shake.c ../randombytes.c $(LDFLAGS)

clean:
	rm -f benchmark_original benchmark_tweaked results_*.txt
