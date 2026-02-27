#!/bin/bash

# NSE Prediction Agent - Verification Script
# Checks if all dependencies are installed and working

echo "🔍 NSE Prediction Agent - System Verification"
echo "=============================================="
echo ""

PROJECT_DIR="/Users/ambujgoel_macpro/Ambuj-Local-code/nse-analysis"
VENV="$PROJECT_DIR/venv/bin/activate"

# Check if venv exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "❌ Virtual environment not found"
    echo "   Run: bash setup.sh"
    exit 1
fi

# Activate venv
source "$VENV"

echo "✅ Virtual environment activated"
echo ""

# Test each import
echo "Testing imports..."
echo "===================="

$PROJECT_DIR/venv/bin/python3 -c "import yfinance; print('✓ yfinance')" 2>&1 || echo "✗ yfinance"
$PROJECT_DIR/venv/bin/python3 -c "import pandas; print('✓ pandas')" 2>&1 || echo "✗ pandas"
$PROJECT_DIR/venv/bin/python3 -c "import numpy; print('✓ numpy')" 2>&1 || echo "✗ numpy"
$PROJECT_DIR/venv/bin/python3 -c "import sklearn; print('✓ scikit-learn')" 2>&1 || echo "✗ scikit-learn"
$PROJECT_DIR/venv/bin/python3 -c "import xgboost; print('✓ xgboost')" 2>&1 || echo "✗ xgboost"
$PROJECT_DIR/venv/bin/python3 -c "import talib; print('✓ ta-lib')" 2>&1 || echo "✗ ta-lib"
$PROJECT_DIR/venv/bin/python3 -c "import joblib; print('✓ joblib')" 2>&1 || echo "✗ joblib"
$PROJECT_DIR/venv/bin/python3 -c "import APScheduler; print('✓ APScheduler')" 2>&1 || echo "✗ APScheduler"

echo ""
echo "Testing configuration files..."
echo "=============================="

[ -f "$PROJECT_DIR/config.py" ] && echo "✓ config.py" || echo "✗ config.py"
[ -f "$PROJECT_DIR/.env" ] && echo "✓ .env" || echo "✗ .env (optional)"
[ -f "$PROJECT_DIR/agent.py" ] && echo "✓ agent.py" || echo "✗ agent.py"
[ -f "$PROJECT_DIR/scheduler.py" ] && echo "✓ scheduler.py" || echo "✗ scheduler.py"
[ -f "$PROJECT_DIR/quickstart.py" ] && echo "✓ quickstart.py" || echo "✗ quickstart.py"

echo ""
echo "Testing directories..."
echo "======================"

[ -d "$PROJECT_DIR/data" ] && echo "✓ data/" || mkdir -p "$PROJECT_DIR/data" && echo "✓ data/ (created)"
[ -d "$PROJECT_DIR/models" ] && echo "✓ models/" || mkdir -p "$PROJECT_DIR/models" && echo "✓ models/ (created)"
[ -d "$PROJECT_DIR/logs" ] && echo "✓ logs/" || mkdir -p "$PROJECT_DIR/logs" && echo "✓ logs/ (created)"

echo ""
echo "=============================================="
echo "✅ Verification Complete!"
echo "=============================================="
echo ""
echo "📖 Ready to use. Next steps:"
echo ""
echo "1. Activate environment:"
echo "   source $PROJECT_DIR/venv/bin/activate"
echo ""
echo "2. Run example:"
echo "   python quickstart.py 1"
echo ""
echo "3. Train model:"
echo "   python agent.py --train"
echo ""
echo "4. Make predictions:"
echo "   python agent.py --predict"
echo ""
