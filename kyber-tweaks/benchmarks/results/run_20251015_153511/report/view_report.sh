#!/bin/bash
# Quick report viewer

# Try to open in default browser
if command -v xdg-open > /dev/null; then
    xdg-open benchmark_report.html
elif command -v open > /dev/null; then
    open benchmark_report.html
else
    echo "Please open benchmark_report.html in your web browser"
    echo "Full path: $(pwd)/benchmark_report.html"
fi
