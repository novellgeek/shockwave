#!/bin/bash
# SHOCKWAVE PLANNER v1.1 Quick Start Script

echo "=========================================="
echo "  SHOCKWAVE PLANNER v1.1"
echo "  Launch Operations Planning System"
echo "=========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for PyQt6
echo "Checking for PyQt6..."
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "⚠ PyQt6 not found. Installing..."
    pip install PyQt6 --break-system-packages
else
    echo "✓ PyQt6 is installed"
fi

echo ""
echo "Starting SHOCKWAVE PLANNER v1.1..."
echo ""

# Run the application
python3 main.py

echo ""
echo "Application closed."
