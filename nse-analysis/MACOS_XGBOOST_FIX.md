# macOS Setup - XGBoost Fix

If you see XGBoost or scipy import errors on macOS, follow this fix:

## Issue
On macOS, XGBoost requires the OpenMP library (`libomp`), which may not be installed.

## Solution

### Step 1: Install libomp via Homebrew
```bash
brew install libomp
```

### Step 2: Add environment variables to your shell profile

Add these lines to `~/.zshrc` (or `~/.bash_profile` if using bash):

```bash
# For XGBoost and other scientific packages
export LDFLAGS="-L/usr/local/opt/libomp/lib"
export CPPFLAGS="-I/usr/local/opt/libomp/include"
export DYLD_LIBRARY_PATH="/usr/local/opt/libomp/lib:$DYLD_LIBRARY_PATH"
```

### Step 3: Reload your shell
```bash
# Reload shell configuration
source ~/.zshrc

# Or restart terminal
```

### Step 4: Activate venv and verify
```bash
cd /Users/ambujgoel_macpro/Ambuj-Local-code/nse-analysis
source venv/bin/activate

# Test import
python3 -c "import xgboost; print('✅ XGBoost working!')"
```

## Alternative: Use Random Forest (No XGBoost)

If you still have issues with XGBoost, you can use Random Forest instead:

1. Edit `config.py`:
```python
MODEL_TYPE = "random_forest"  # Instead of "xgboost"
```

2. For prediction only (no training), skip this and just predict with:
```bash
python agent.py --predict
```

Random Forest works the same way and has ~70% accuracy too.

## Quick Test

After setup, test with:
```bash
source venv/bin/activate
python agent.py --predict
```

This analyzes yesterday's data and makes a prediction (doesn't need XGBoost until model training).

## If Still Having Issues

Try reinstalling with:
```bash
source venv/bin/activate
pip uninstall xgboost scipy -y
pip install --no-cache-dir xgboost scipy
```

Then restart terminal and try again.

---

**Note**: Most issues are resolved by installing libomp and adding the environment variables to your shell profile.
