markdown
# Kyber CLI Tests

This directory contains command-line tools and scripts to demonstrate Kyber parameter tweaks and their impacts.

## Tools

### Core Utilities

1. **kyber_keygen** - Generate Kyber keypairs
   ```bash
   ./kyber_keygen -p -v              # Show parameters and generate keys
   ./kyber_keygen -o mykey -f hex    # Generate and display in hex
kyber_encrypt - Encrypt using Kyber KEM

bash
./kyber_encrypt -k key.pub -v     # Encrypt with verbose output
./kyber_encrypt -k key.pub -f hex # Show ciphertext in hex
kyber_decrypt - Decrypt Kyber ciphertext

bash
./kyber_decrypt -s key.sec -c ciphertext.bin -v
kyber_demo - Interactive demonstration

bash
./kyber_demo      # Interactive mode
./kyber_demo -q   # Quick mode
Scripts
test_all_params.sh - Test all parameter configurations

bash
./scripts/test_all_params.sh
compare_sizes.sh - Compare ciphertext sizes

bash
./scripts/compare_sizes.sh
demo_tweaks.sh - Interactive parameter demonstration

bash
./scripts/demo_tweaks.sh
Parameter Configurations
The following parameter sets are tested:

Configuration	(du, dv)	Ciphertext Impact	Performance Impact
Baseline	(10, 4)	768 bytes (ref)	Reference
Test 1	(10, 4)	No change	No change
Test 2	(11, 3)	-32 bytes (-4.2%)	~2-5% overhead
Test 3	(9, 5)	+32 bytes (+4.2%)	~10-15% overhead
Test 4	Eta mods	No change	~20-30% overhead
Quick Start
Build all tools:

bash
make all
Run a complete test:

bash
# Generate keys
./kyber_keygen -v

# Encrypt
./kyber_encrypt -k kyber_key.pub -v

# Decrypt
./kyber_decrypt -s kyber_key.sec -c ciphertext.bin -v

# Verify
cmp shared_secret.bin decrypted_secret.bin
Compare configurations:

bash
./scripts/compare_sizes.sh
Understanding Results
Ciphertext Size: Directly affected by (du, dv) compression parameters
Performance: Trade-off between size and computational overhead
Eta Parameters: Affect security margin and performance, not sizes
Building for Different Variants
bash
make clean && make kyber512   # Build for Kyber512
make clean && make kyber768   # Build for Kyber768
make clean && make kyber1024  # Build for Kyber1024
text

Test the interactive demo:

```bash
./scripts/demo_tweaks.sh
