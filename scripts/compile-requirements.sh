#!/bin/bash

# Compile requirements for different Python versions
# This ensures compatibility across our supported Python version matrix

set -e

echo "🔨 Compiling requirements for multiple Python versions..."

# Function to compile requirements with specific Python version
compile_for_python() {
    local python_version=$1
    local suffix=$2
    
    echo "📋 Compiling for Python $python_version..."
    
    # Use specific Python version if available, otherwise use current
    if command -v python$python_version &> /dev/null; then
        python_cmd="python$python_version"
    else
        echo "⚠️  Python $python_version not found, using current Python"
        python_cmd="python"
    fi
    
    # Compile requirements
    $python_cmd -m pip install pip-tools
    $python_cmd -m piptools compile --upgrade --strip-extras requirements/base.in --output-file requirements/base$suffix.txt
    $python_cmd -m piptools compile --upgrade --strip-extras requirements/dev.in --output-file requirements/dev$suffix.txt
    $python_cmd -m piptools compile --upgrade --strip-extras requirements/production.in --output-file requirements/production$suffix.txt
}

# Clean existing compiled files
echo "🧹 Cleaning existing compiled requirements..."
rm -f requirements/*.txt

# Compile for Python 3.10 (minimum supported)
if command -v python3.10 &> /dev/null; then
    compile_for_python "3.10" "-py310"
    
    # Use Python 3.10 compiled requirements as the default
    cp requirements/base-py310.txt requirements/base.txt
    cp requirements/dev-py310.txt requirements/dev.txt
    cp requirements/production-py310.txt requirements/production.txt
    
    echo "✅ Using Python 3.10 compiled requirements as default"
else
    echo "⚠️  Python 3.10 not available, compiling with current Python"
    compile_for_python "" ""
fi

# Compile for other versions if available
for version in "3.11" "3.12"; do
    if command -v python$version &> /dev/null; then
        compile_for_python "$version" "-py${version//.}"
    else
        echo "⚠️  Python $version not available, skipping"
    fi
done

echo "✅ Requirements compilation complete!"
echo "📁 Generated files:"
ls -la requirements/*.txt
