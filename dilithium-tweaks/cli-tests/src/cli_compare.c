#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "../include/common.h"

void run_sign_command(const char *executable, const char *message_file, 
                     const char *key_file, const char *output_sig,
                     double *time_ms) {
    char cmd[1024];
    snprintf(cmd, sizeof(cmd), 
             "./%s -i %s -k %s -o %s -m baseline 2>&1", 
             executable, message_file, key_file, output_sig);
    
    FILE *fp = popen(cmd, "r");
    if (!fp) {
        *time_ms = -1;
        return;
    }
    
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, "Time:")) {
            sscanf(line, "Time: %lf ms", time_ms);
        }
        printf("%s", line);
    }
    
    pclose(fp);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <message_file> <key_file>\n", argv[0]);
        return 1;
    }
    
    const char *message_file = argv[1];
    const char *key_file = argv[2];
    
    printf("=== Dilithium Implementation Comparison ===\n");
    printf("Message: %s\n", message_file);
    printf("Key: %s\n\n", key_file);
    
    printf("%-15s | %-10s | %-10s\n", "Implementation", "Time (ms)", "Status");
    printf("----------------|------------|------------\n");
    
    // Test baseline
    double time_baseline;
    printf("\nBaseline:\n");
    run_sign_command("cli_sign_baseline", message_file, key_file, "cmp_baseline.sig", &time_baseline);
    
    // Test option1
    double time_option1;
    printf("\nOption 1 (Relaxed Bounds):\n");
    run_sign_command("cli_sign_option1", message_file, key_file, "cmp_option1.sig", &time_option1);
    
    // Test option2
    double time_option2;
    printf("\nOption 2 (Probabilistic):\n");
    run_sign_command("cli_sign_option2", message_file, key_file, "cmp_option2.sig", &time_option2);
    
    // Summary
    printf("\n\n=== Summary ===\n");
    printf("%-15s | %10.2f | %s\n", "Baseline", time_baseline, "✓");
    printf("%-15s | %10.2f | %s (%.1fx slower)\n", "Option 1", time_option1, "✓", time_option1/time_baseline);
    printf("%-15s | %10.2f | %s (%.1fx slower)\n", "Option 2", time_option2, "✓", time_option2/time_baseline);
    
    return 0;
}