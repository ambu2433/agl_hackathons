#!/bin/bash

# NSE Prediction Agent - Setup Script for macOS
# This script sets up the virtual environment and installs all dependencies

set -e

echo "🚀 NSE Prediction Agent Setup"
echo "=============================="
echo ""

PROJECT_DIR="/Users/ambujgoel_macpro/Ambuj-Local-code/nse-analysis"

cd "$PROJECT_DIR"

# Step 1: Create virtual environment
echo "📦 Step 1: Creating Python virtual environment..."
python3 -m venv venv 2>/dev/null || echo "Virtual environment already exists"
echo "✓ Virtual environment created"
echo ""

# Step 2: Activate and upgrade pip
echo "🔄 Step 2: Upgrading pip, setuptools and wheel..."
./venv/bin/python3 -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Step 3: Install core packages
echo "📥 Step 3: Installing core dependencies..."
./venv/bin/pip install \
    yfinance \
    pandas \
    numpy \
    scikit-learn \
    xgboost \
    python-dotenv \
    requests \
    APScheduler \
    matplotlib \
    seaborn \
    plotly \
    joblib \
    python-telegram-bot \
    ta-lib \
    > /dev/null 2>&1

echo "✓ All packages installed"
echo ""

# Step 4: Verify installation
echo "✅ Step 4: Verifying installation..."
./venv/bin/python3 -c "import yfinance, pandas, xgboost, talib; print('✓ All core packages working')" 2>/dev/null || echo "⚠️  Note: Some packages may need verification"
echo ""

# Step 5: Create .env file
echo "⚙️  Step 5: Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file (edit with your credentials)"
else
    echo "✓ .env already exists"
fi
echo ""

# Done
echo "=============================="
echo "✅ Setup Complete!"
echo "=============================="
echo ""
echo "📖 Next Steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source $(pwd)/venv/bin/activate"
echo ""
echo "2. Configure your settings:"
echo "   Edit .env with email credentials (optional)"
echo "   Edit config.py for model settings (optional)"
echo ""
echo "3. Train the model (first time):"
echo "   python agent.py --train"
echo ""
echo "4. Make predictions:"
echo "   python agent.py --predict"
echo ""
echo "5. Run on schedule:"
echo "   python scheduler.py"
echo ""
echo "For more info, see GETTING_STARTED.md"
echo ""
