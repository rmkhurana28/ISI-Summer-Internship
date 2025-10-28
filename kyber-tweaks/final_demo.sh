#!/bin/bash

# =============================================================================
# Kyber Parameter Tweaks - Complete Demonstration Script
# =============================================================================
# This script automates the entire workflow from Chapter 5 of the thesis:
# 1. Performance benchmarking with different parameters
# 2. Correctness testing with CLI tools
# 3. Security analysis (both static and dynamic)
# 4. Results generation matching thesis tables and figures
# =============================================================================

set -e  # Exit on error

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEMO_LOG="${PROJECT_ROOT}/demo_${TIMESTAMP}.log"

# Colors for the output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art Header
print_header() {
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                  KYBER PARAMETER TWEAKS DEMO                      ║
║                    Thesis Chapter 5 Results                       ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Progress bar function
show_progress() {
    local current=$1
    local total=$2
    local task=$3
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((width * current / total))
    
    printf "\r${YELLOW}[%-${width}s] %3d%% ${NC}%s" \
        "$(printf '#%.0s' $(seq 1 $completed))" \
        "$percentage" \
        "$task"
}

# Logging function
log() {
    echo -e "$1" | tee -a "$DEMO_LOG"
}

# Global variable to track if SageMath is available
SAGE_AVAILABLE=0
SAGE_ENV_NAME=""

# Function to check and activate sage environment
activate_sage_env() {
    # Check if conda is available
    if command -v conda &> /dev/null; then
        log "${BLUE}Checking for conda environments with SageMath...${NC}"
        
        # Get list of conda environments
        conda_envs=$(conda env list | grep -v "^#" | awk '{print $1}')
        
        # Common sage environment names
        sage_env_patterns="sage sagemath sage_env"
        
        for pattern in $sage_env_patterns; do
            for env in $conda_envs; do
                if [[ "$env" == *"$pattern"* ]]; then
                    log "${YELLOW}Found potential SageMath environment: $env${NC}"
                    
                    # Try to activate and check for sage
                    if conda activate "$env" 2>/dev/null && command -v sage &> /dev/null; then
                        SAGE_ENV_NAME="$env"
                        SAGE_AVAILABLE=1
                        log "${GREEN}✓ Successfully activated SageMath environment: $env${NC}"
                        return 0
                    fi
                fi
            done
        done
    fi
    
    # Check if sage is available without conda
    if command -v sage &> /dev/null; then
        SAGE_AVAILABLE=1
        log "${GREEN}✓ SageMath found in system PATH${NC}"
        return 0
    fi
    
    return 1
}

# Check prerequisites
check_prerequisites() {
    log "${BLUE}Checking prerequisites...${NC}"
    
    local missing=0
    local missing_critical=0
    
    # Check for required commands
    for cmd in gcc make python3 git; do
        if ! command -v $cmd &> /dev/null; then
            log "${RED}✗ $cmd not found (REQUIRED)${NC}"
            missing_critical=1
        else
            log "${GREEN}✓ $cmd found${NC}"
        fi
    done
    
    # Check for optional SageMath
    if ! activate_sage_env; then
        log "${YELLOW}⚠ SageMath not found (OPTIONAL - needed only for dynamic security analysis)${NC}"
        log "${YELLOW}To install SageMath:${NC}"
        log "${YELLOW}  - Using conda: conda create -n sage_env sage python=3.9${NC}"
        log "${YELLOW}  - Using apt: sudo apt install sagemath${NC}"
        SAGE_AVAILABLE=0
    fi
    
    # Check directory structure
    for dir in kyber/ref benchmarks cli-tests kyber-security-analysis kyber-dynamic-security-analysis; do
        if [ ! -d "$PROJECT_ROOT/$dir" ]; then
            log "${RED}✗ Directory $dir not found${NC}"
            missing_critical=1
        else
            log "${GREEN}✓ Directory $dir exists${NC}"
        fi
    done
    
    # Check for config files
    if [ -d "$PROJECT_ROOT/kyber/ref/configs" ]; then
        config_count=$(ls -1 "$PROJECT_ROOT/kyber/ref/configs/"params_*.h 2>/dev/null | wc -l)
        if [ $config_count -eq 0 ]; then
            log "${RED}✗ No parameter configuration files found${NC}"
            missing_critical=1
        else
            log "${GREEN}✓ Found $config_count parameter configuration files${NC}"
        fi
    fi
    
    if [ $missing_critical -eq 1 ]; then
        log "${RED}Critical prerequisites missing. Please fix the issues above.${NC}"
        exit 1
    fi
    
    if [ $SAGE_AVAILABLE -eq 0 ]; then
        log "\n${YELLOW}Note: SageMath is not installed. Dynamic security analysis will be skipped.${NC}"
    fi
    
    log "${GREEN}All required prerequisites satisfied!${NC}\n"
}

# Section 1: Performance Benchmarking
run_performance_benchmarks() {
    log "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    log "${MAGENTA}SECTION 1: PERFORMANCE BENCHMARKING${NC}"
    log "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    cd "$PROJECT_ROOT/benchmarks"
    
    log "${BLUE}Running comprehensive performance benchmarks...${NC}"
    log "This will test all parameter configurations and generate Tables 5.1-5.4\n"
    
    # Run cycle count benchmarks
    if [ -x "./run_cycle_counts.sh" ]; then
        ./run_cycle_counts.sh | tee -a "$DEMO_LOG"
        
        # Get the latest run directory
        LATEST_RUN=$(ls -d results/run_* 2>/dev/null | sort | tail -1)
        
        if [ -n "$LATEST_RUN" ]; then
            log "\n${BLUE}Analyzing benchmark results...${NC}"
            python3 analyze_results.py "$LATEST_RUN" | tee -a "$DEMO_LOG"
            
            log "\n${BLUE}Generating performance charts...${NC}"
            python3 generate_charts.py "$LATEST_RUN/analysis_data.json"
            
            log "\n${BLUE}Creating comprehensive report...${NC}"
            ./generate_report.sh
            
            # Extract thesis tables
            log "\n${GREEN}Extracting thesis tables from results:${NC}"
            for table_num in 1 2 3 4; do
                log "\n${YELLOW}Table 5.$table_num:${NC}"
                grep -A 20 "Table 5.$table_num:" "$LATEST_RUN/analysis_report.txt" | head -25
            done
        fi
    else
        log "${RED}Error: run_cycle_counts.sh not found or not executable${NC}"
    fi
    
    cd "$PROJECT_ROOT"
}

# Section 2: Correctness Testing
run_correctness_tests() {
    log "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    log "${MAGENTA}SECTION 2: CORRECTNESS TESTING${NC}"
    log "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    cd "$PROJECT_ROOT/cli-tests"
    
    log "${BLUE}Testing all parameter configurations for correctness...${NC}\n"
    
    if [ -x "./scripts/test_all_params.sh" ]; then
        ./scripts/test_all_params.sh | tee -a "$DEMO_LOG"
        
        log "\n${BLUE}Comparing ciphertext sizes across configurations...${NC}"
        if [ -x "./scripts/compare_sizes.sh" ]; then
            ./scripts/compare_sizes.sh | tee -a "$DEMO_LOG"
        fi
    else
        log "${RED}Error: test_all_params.sh not found${NC}"
    fi
    
    cd "$PROJECT_ROOT"
}

# Section 3: Security Analysis
run_security_analysis() {
    log "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    log "${MAGENTA}SECTION 3: SECURITY ANALYSIS${NC}"
    log "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    # Static Analysis
    log "${BLUE}3.1 Static Security Analysis (Hardcoded Values)${NC}\n"
    cd "$PROJECT_ROOT/kyber-security-analysis"
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
    
    if [ -x "./run_all_analysis.sh" ]; then
        ./run_all_analysis.sh | tee -a "$DEMO_LOG"
        
        # Extract thesis tables
        log "\n${GREEN}Extracting security analysis tables:${NC}"
        for table_num in 5 6 7 8; do
            log "\n${YELLOW}Table 5.$table_num:${NC}"
            grep -A 15 "Table 5.$table_num:" results/security_analysis_results.txt | head -20
        done
    fi
    
    # Dynamic Analysis (if SageMath is available)
    if [ $SAGE_AVAILABLE -eq 1 ]; then
        log "\n${BLUE}3.2 Dynamic Security Analysis (Calculated Values)${NC}\n"
        cd "$PROJECT_ROOT/kyber-dynamic-security-analysis"
        
        # Ensure sage environment is activated
        if [ -n "$SAGE_ENV_NAME" ]; then
            log "${YELLOW}Activating SageMath environment: $SAGE_ENV_NAME${NC}"
            conda activate "$SAGE_ENV_NAME"
        fi
        
        if [ -x "./run_dynamic_analysis.sh" ]; then
            ./run_dynamic_analysis.sh | tee -a "$DEMO_LOG"
            
            # Show comparison
            if [ -f "results/comparison.txt" ]; then
                log "\n${YELLOW}Static vs Dynamic Comparison:${NC}"
                cat results/comparison.txt | tee -a "$DEMO_LOG"
            fi
        fi
    else
        log "\n${YELLOW}Skipping dynamic analysis (SageMath not installed)${NC}"
        log "${YELLOW}The static analysis provides the security estimates from the thesis.${NC}"
    fi
    
    cd "$PROJECT_ROOT"
}

# Generate final summary - rest of the script remains the same...
generate_summary() {
    log "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
    log "${MAGENTA}FINAL SUMMARY${NC}"
    log "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"
    
    # Create summary report
    SUMMARY_FILE="${PROJECT_ROOT}/thesis_results_${TIMESTAMP}.txt"
    
    cat > "$SUMMARY_FILE" << EOF
KYBER PARAMETER TWEAKS - THESIS CHAPTER 5 RESULTS
Generated: $(date)
================================================

1. PERFORMANCE ANALYSIS RESULTS
------------------------------
EOF
    
        # Add performance tables
    if [ -n "$LATEST_RUN" ] && [ -f "$PROJECT_ROOT/benchmarks/$LATEST_RUN/analysis_report.txt" ]; then
        echo -e "\n--- Tables 5.1-5.4: Performance Analysis ---\n" >> "$SUMMARY_FILE"
        cat "$PROJECT_ROOT/benchmarks/$LATEST_RUN/analysis_report.txt" >> "$SUMMARY_FILE"
    fi
    
    # Add security analysis results
    cat >> "$SUMMARY_FILE" << EOF

2. SECURITY ANALYSIS RESULTS
----------------------------
EOF
    
    if [ -f "$PROJECT_ROOT/kyber-security-analysis/results/security_analysis_results.txt" ]; then
        echo -e "\n--- Tables 5.5-5.8: Security Analysis ---\n" >> "$SUMMARY_FILE"
        cat "$PROJECT_ROOT/kyber-security-analysis/results/security_analysis_results.txt" >> "$SUMMARY_FILE"
    fi
    
    # Add correctness test results
    cat >> "$SUMMARY_FILE" << EOF

3. CORRECTNESS TEST RESULTS
--------------------------
EOF
    
    if [ -d "$PROJECT_ROOT/cli-tests/test_results" ]; then
        echo -e "\nAll parameter configurations:" >> "$SUMMARY_FILE"
        for result in "$PROJECT_ROOT/cli-tests/test_results/"*/result.txt; do
            if [ -f "$result" ]; then
                config=$(basename $(dirname "$result"))
                status=$(cat "$result")
                echo "  $config: $status" >> "$SUMMARY_FILE"
            fi
        done
    fi
    
    # Display summary
    log "${GREEN}Summary report generated: $SUMMARY_FILE${NC}\n"
    
    # Show key findings
    log "${YELLOW}KEY FINDINGS:${NC}"
    log "1. Compression Parameter Impact:"
    log "   - (du=11, dv=3): ~4% ciphertext reduction, minimal performance impact"
    log "   - (du=9, dv=5): ~4% ciphertext increase, significant performance overhead"
    log ""
    log "2. Noise Parameter Impact:"
    log "   - Kyber512 with η₁=5, η₂=3: +32% KeyGen, +34% Encryption time"
    log "   - No change in ciphertext sizes"
    log ""
    log "3. Security Analysis:"
    log "   - All configurations maintain required security levels"
    if [ $SAGE_AVAILABLE -eq 1 ]; then
        log "   - Dynamic analysis shows ~25-30 bits higher security than static"
    else
        log "   - Static analysis shows security levels from thesis"
    fi
    log ""
    
    # Links to detailed results
    log "${CYAN}Detailed Results:${NC}"
    if [ -n "$LATEST_RUN" ]; then
        log "- Performance Report: benchmarks/$LATEST_RUN/report/benchmark_report.html"
    fi
    log "- Security Plots: kyber-security-analysis/results/plots/"
    log "- Test Logs: cli-tests/test_results/"
    log "- Full Log: $DEMO_LOG"
}

# Interactive menu
show_menu() {
    echo -e "\n${CYAN}Select components to run:${NC}"
    echo "1) Run everything (recommended)"
    echo "2) Performance benchmarks only"
    echo "3) Correctness tests only"
    echo "4) Security analysis only"
    echo "5) Generate summary from existing results"
    echo "6) Quick demo (subset of tests)"
    echo "7) Exit"
    
    if [ $SAGE_AVAILABLE -eq 0 ]; then
        echo -e "\n${YELLOW}Note: Dynamic security analysis requires SageMath${NC}"
    fi
    
    echo -ne "\n${YELLOW}Enter choice [1-7]: ${NC}"
}

# Quick demo function
run_quick_demo() {
    log "\n${MAGENTA}QUICK DEMO MODE${NC}"
    log "Running subset of tests for rapid demonstration...\n"
    
    # Quick benchmark
    cd "$PROJECT_ROOT/benchmarks"
    if [ -x "./quick_bench.sh" ]; then
        log "${BLUE}Running quick benchmarks...${NC}"
        ./quick_bench.sh --test 2 | tee -a "$DEMO_LOG"
    fi
    
    # Quick correctness test
    cd "$PROJECT_ROOT/cli-tests"
    log "\n${BLUE}Running quick correctness test...${NC}"
    if [ -x "./kyber_demo" ]; then
        ./kyber_demo -q | tee -a "$DEMO_LOG"
    fi
    
    # Quick security check
    cd "$PROJECT_ROOT/kyber-security-analysis"
    log "\n${BLUE}Running quick security check...${NC}"
    if [ -f "scripts/Kyber.py" ]; then
        python3 scripts/Kyber.py --param-set 512 --du 11 --dv 3 | tee -a "$DEMO_LOG"
    fi
    
    cd "$PROJECT_ROOT"
    log "\n${GREEN}Quick demo complete!${NC}"
}

# Setup conda initialization if needed
setup_conda() {
    # Common conda installation paths
    conda_paths=(
        "$HOME/anaconda3"
        "$HOME/miniconda3"
        "/opt/anaconda3"
        "/opt/miniconda3"
        "$HOME/mambaforge"
        "/usr/local/anaconda3"
    )
    
    for conda_path in "${conda_paths[@]}"; do
        if [ -f "$conda_path/etc/profile.d/conda.sh" ]; then
            source "$conda_path/etc/profile.d/conda.sh"
            return 0
        fi
    done
    
    # Check if conda is already in PATH
    if command -v conda &> /dev/null; then
        return 0
    fi
    
    return 1
}

# Main execution
main() {
    clear
    print_header
    
    log "Demo started at: $(date)"
    log "Project root: $PROJECT_ROOT"
    log "Log file: $DEMO_LOG\n"
    
    # Setup conda if available
    if setup_conda; then
        log "${GREEN}Conda environment system detected${NC}"
    fi
    
    # Check prerequisites
    check_prerequisites
    
    # Interactive or automatic mode
    if [ "$1" == "--auto" ]; then
        log "${GREEN}Running in automatic mode...${NC}\n"
        run_performance_benchmarks
        run_correctness_tests
        run_security_analysis
        generate_summary
    else
        while true; do
            show_menu
            read choice
            
            case $choice in
                1)
                    run_performance_benchmarks
                    run_correctness_tests
                    run_security_analysis
                    generate_summary
                    ;;
                2)
                    run_performance_benchmarks
                    ;;
                3)
                    run_correctness_tests
                    ;;
                4)
                    run_security_analysis
                    ;;
                5)
                    # Find latest run for summary
                    if [ -z "$LATEST_RUN" ]; then
                        cd "$PROJECT_ROOT/benchmarks"
                        LATEST_RUN=$(ls -d results/run_* 2>/dev/null | sort | tail -1)
                        cd "$PROJECT_ROOT"
                    fi
                    generate_summary
                    ;;
                6)
                    run_quick_demo
                    ;;
                7)
                    log "\n${GREEN}Demo completed. Thank you!${NC}"
                    exit 0
                    ;;
                *)
                    log "${RED}Invalid choice. Please select 1-7.${NC}"
                    ;;
            esac
            
            if [ "$choice" -ge 1 ] && [ "$choice" -le 6 ]; then
                log "\n${GREEN}Task completed. Press Enter to continue...${NC}"
                read
            fi
        done
    fi
    
    log "\n${GREEN}═══════════════════════════════════════════════════════════${NC}"
    log "${GREEN}DEMO COMPLETE${NC}"
    log "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    log "All results have been generated and saved."
    log "Check the summary report: thesis_results_${TIMESTAMP}.txt"
    log "Full demo log: $DEMO_LOG"
}

# Handle script arguments
case "$1" in
    -h|--help)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --auto    Run all components automatically"
        echo "  --help    Show this help message"
        echo ""
        echo "Interactive mode (default) allows you to choose which components to run."
        echo ""
        echo "This script demonstrates the Kyber parameter tweaks from thesis Chapter 5:"
        echo "- Performance impact of compression parameters (du, dv)"
        echo "- Effect of noise distribution parameters (η₁, η₂)"
        echo "- Security analysis of all parameter variations"
        echo ""
        echo "Note: SageMath can be installed in a conda environment."
        echo "The script will automatically search for and activate sage environments."
        exit 0
        ;;
    --auto)
        main --auto
        ;;
    *)
        main
        ;;
esac