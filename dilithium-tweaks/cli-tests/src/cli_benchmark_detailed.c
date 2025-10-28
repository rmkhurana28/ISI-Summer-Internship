#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include "../include/common.h"

#define NUM_RUNS 100
#define WARMUP_RUNS 10

typedef struct {
    double min;
    double max;
    double mean;
    double median;
    double stddev;
    double percentile_95;
} stats_t;

typedef struct {
    const char *name;
    const char *executable;
    double median_times[3];
} impl_results_t;

int compare_double(const void *a, const void *b) {
    double diff = *(double*)a - *(double*)b;
    return (diff > 0) - (diff < 0);
}

void calculate_stats(double *times, int count, stats_t *stats) {
    qsort(times, count, sizeof(double), compare_double);
    
    stats->min = times[0];
    stats->max = times[count - 1];
    
    if (count % 2 == 0) {
        stats->median = (times[count/2 - 1] + times[count/2]) / 2.0;
    } else {
        stats->median = times[count/2];
    }
    
    double sum = 0;
    for (int i = 0; i < count; i++) {
        sum += times[i];
    }
    stats->mean = sum / count;
    
    double sum_sq = 0;
    for (int i = 0; i < count; i++) {
        double diff = times[i] - stats->mean;
        sum_sq += diff * diff;
    }
    stats->stddev = sqrt(sum_sq / count);
    
    int idx_95 = (int)(0.95 * count);
    stats->percentile_95 = times[idx_95];
}

double benchmark_implementation(const char *name, const char *executable, 
                               const char *message_file, const char *key_file) {
    printf("\n=== Benchmarking %s ===\n", name);
    
    double *times = malloc(NUM_RUNS * sizeof(double));
    if (!times) {
        fprintf(stderr, "Memory allocation failed\n");
        return -1;
    }
    
    printf("Warming up...");
    fflush(stdout);
    for (int i = 0; i < WARMUP_RUNS; i++) {
        char cmd[1024];
        snprintf(cmd, sizeof(cmd), "./%s -i %s -k %s -o temp.sig -m baseline >/dev/null 2>&1", 
                 executable, message_file, key_file);
        system(cmd);
    }
    printf(" done\n");
    
    printf("Running %d iterations...\n", NUM_RUNS);
    for (int i = 0; i < NUM_RUNS; i++) {
        double start = get_time_ms();
        
        char cmd[1024];
        snprintf(cmd, sizeof(cmd), "./%s -i %s -k %s -o temp.sig -m baseline >/dev/null 2>&1", 
                 executable, message_file, key_file);
        system(cmd);
        
        double end = get_time_ms();
        times[i] = end - start;
        
        if ((i + 1) % 10 == 0) {
            printf(".");
            fflush(stdout);
        }
    }
    printf(" done\n");
    
    stats_t stats;
    calculate_stats(times, NUM_RUNS, &stats);
    
    printf("\nResults for %s:\n", name);
    printf("  Minimum:      %6.2f ms\n", stats.min);
    printf("  Median:       %6.2f ms\n", stats.median);
    printf("  Mean:         %6.2f ms\n", stats.mean);
    printf("  Maximum:      %6.2f ms\n", stats.max);
    printf("  Std Dev:      %6.2f ms\n", stats.stddev);
    printf("  95%%ile:      %6.2f ms\n", stats.percentile_95);
    
    double median_result = stats.median;
    free(times);
    return median_result;
}

int main(int argc, char *argv[]) {
    if (access("output/keys/bench_key.sk", F_OK) != 0) {
        printf("Generating benchmark keys...\n");
        system("./cli_keygen_simple -o bench_key");
    }
    
    const char *message_files[] = {
        "test_data/messages/short.txt",
        "test_data/messages/medium.txt",
        "test_data/messages/large.txt"
    };
    
    const char *message_names[] = {
        "Short (46 bytes)",
        "Medium (~200 bytes)",
        "Large (~20KB)"
    };
    
    impl_results_t results[] = {
        {"Baseline", "cli_sign_baseline", {0, 0, 0}},
        {"Option 1 (Relaxed Bounds)", "cli_sign_option1", {0, 0, 0}},
        {"Option 2 (Probabilistic)", "cli_sign_option2", {0, 0, 0}}
    };
    
    for (int msg = 0; msg < 3; msg++) {
        if (access(message_files[msg], F_OK) != 0) {
            printf("\nSkipping %s - file not found\n", message_files[msg]);
            continue;
        }
        
        printf("\n");
        printf("===========================================\n");
        printf("Message: %s\n", message_names[msg]);
        printf("===========================================\n");
        
        for (int impl = 0; impl < 3; impl++) {
            results[impl].median_times[msg] = benchmark_implementation(
                results[impl].name, 
                results[impl].executable,
                message_files[msg], 
                "output/keys/bench_key.sk"
            );
        }
    }
    
    printf("\n\n=== Summary Table ===\n");
    printf("All times are median values from %d runs\n", NUM_RUNS);
    printf("%-20s | %-10s | %-10s | %-10s | %-12s\n", 
           "Implementation", "Short msg", "Medium msg", "Large msg", "Avg Slowdown");
    printf("---------------------|------------|------------|------------|-------------\n");
    
    for (int impl = 0; impl < 3; impl++) {
        double avg_slowdown = 0;
        int valid_count = 0;
        
        for (int msg = 0; msg < 3; msg++) {
            if (results[impl].median_times[msg] > 0 && results[0].median_times[msg] > 0) {
                avg_slowdown += results[impl].median_times[msg] / results[0].median_times[msg];
                valid_count++;
            }
        }
        
        if (valid_count > 0) {
            avg_slowdown /= valid_count;
        } else {
            avg_slowdown = 1.0;
        }
        
        printf("%-20s | %7.2f ms | %7.2f ms | %7.2f ms |    %5.1fx\n",
               results[impl].name,
               results[impl].median_times[0],
               results[impl].median_times[1],
               results[impl].median_times[2],
               avg_slowdown);
    }
    
    return 0;
}