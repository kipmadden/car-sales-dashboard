#!/bin/bash

# Development environment setup script
# This script sets up the development environment with all necessary dependencies

set -e

echo "🚀 Setting up Car Sales Dashboard development environment..."

# Check if Python 3.9+ is available
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install pip-tools for dependency management
echo "🛠️ Installing pip-tools..."
pip install pip-tools

# Compile requirements
echo "📋 Compiling requirements..."
pip-compile requirements/base.in
pip-compile requirements/dev.in
pip-compile requirements/production.in

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -r requirements/dev.txt

# Install pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Initialize Reflex
echo "🎯 Initializing Reflex..."
reflex init --template blank

echo "✅ Development environment setup complete!"
echo ""
echo "To activate the environment, run: source venv/bin/activate"
echo "To start the development server, run: reflex run"
echo "To run tests, run: pytest"
echo "To check code quality, run: pre-commit run --all-files"
