#!/bin/bash

# NSE Prediction Agent - macOS Setup & Configuration
# Complete setup with environment variables for XGBoost

set -e

echo "🚀 NSE Prediction Agent - Complete Setup"
echo "=========================================="
echo ""

PROJECT_DIR="/Users/ambujgoel_macpro/Ambuj-Local-code/nse-analysis"

# Determine which shell profile to use
if [ -n "$ZSH_VERSION" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
    echo "Detected: zsh (using ~/.zshrc)"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
    echo "Detected: bash (using ~/.bash_profile)"
else
    SHELL_PROFILE="$HOME/.zshrc"  # Default to zsh
    echo "Detected: unknown shell (using ~/.zshrc)"
fi

echo "Shell profile: $SHELL_PROFILE"
echo ""

# Step 1: Install libomp
echo "📦 Step 1: Installing libomp for XGBoost..."
if command -v brew &> /dev/null; then
    brew install libomp > /dev/null 2>&1 || echo "libomp already installed"
    echo "✓ libomp installed"
else
    echo "⚠️  Homebrew not found. Install from https://brew.sh/"
fi
echo ""

# Step 2: Add environment variables to shell profile
echo "⚙️  Step 2: Configuring shell environment..."

# Create the environment variable block
ENV_VARS="
# XGBoost and scientific packages configuration
export LDFLAGS=\"-L/usr/local/opt/libomp/lib\"
export CPPFLAGS=\"-I/usr/local/opt/libomp/include\"
export DYLD_LIBRARY_PATH=\"/usr/local/opt/libomp/lib:\$DYLD_LIBRARY_PATH\""

# Check if already in profile
if grep -q "LDFLAGS.*libomp" "$SHELL_PROFILE" 2>/dev/null; then
    echo "✓ Environment variables already configured"
else
    echo "" >> "$SHELL_PROFILE"
    echo "# XGBoost and scientific packages configuration" >> "$SHELL_PROFILE"
    echo "export LDFLAGS=\"-L/usr/local/opt/libomp/lib\"" >> "$SHELL_PROFILE"
    echo "export CPPFLAGS=\"-I/usr/local/opt/libomp/include\"" >> "$SHELL_PROFILE"
    echo "export DYLD_LIBRARY_PATH=\"/usr/local/opt/libomp/lib:\$DYLD_LIBRARY_PATH\"" >> "$SHELL_PROFILE"
    echo "✓ Environment variables added to $SHELL_PROFILE"
fi
echo ""

# Step 3: Create virtual environment
cd "$PROJECT_DIR"

echo "📥 Step 3: Setting up Python virtual environment..."
python3 -m venv venv 2>/dev/null || echo "Virtual environment already exists"
echo "✓ Virtual environment ready"
echo ""

# Step 4: Activate and upgrade pip
echo "🔄 Step 4: Upgrading pip..."
./venv/bin/python3 -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Step 5: Install dependencies
echo "📦 Step 5: Installing Python dependencies..."

# Source environment variables for this session
export LDFLAGS="-L/usr/local/opt/libomp/lib"
export CPPFLAGS="-I/usr/local/opt/libomp/include"
export DYLD_LIBRARY_PATH="/usr/local/opt/libomp/lib:$DYLD_LIBRARY_PATH"

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

# Step 6: Create .env file
echo "⚙️  Step 6: Configuration files..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env (edit with your email credentials)"
else
    echo "✓ .env already exists"
fi
echo ""

# Done!
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📝 IMPORTANT: Reload your shell!"
echo ""
echo "Run one of these commands:"
echo ""
echo "  source ~/.zshrc      # if using zsh"
echo "  source ~/.bash_profile  # if using bash"
echo ""
echo "Or simply restart your terminal."
echo ""
echo "🚀 After reloading, you can:"
echo ""
echo "1. Activate environment:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo ""
echo "2. Test data collection:"
echo "   python quickstart.py 1"
echo ""
echo "3. Train model:"
echo "   python agent.py --train"
echo ""
echo "4. Make predictions:"
echo "   python agent.py --predict"
echo ""
echo "5. Schedule daily analysis:"
echo "   python scheduler.py"
echo ""
echo "📖 For more info: cat SETUP_COMPLETE.md"
echo ""
