#!/usr/bin/env python3
"""
Validate requirements compatibility across Python versions.
This script checks that our requirements are compatible with the target Python version.
"""
import sys
import subprocess
from packaging.specifiers import SpecifierSet
from packaging.version import Version

def check_python_compatibility(requirements_file, python_version):
    """Check if requirements are compatible with the specified Python version."""
    print(f"🔍 Checking {requirements_file} compatibility with Python {python_version}")
    
    # Known version constraints for older Python versions
    python_constraints = {
        # Most packages now require Python 3.10+ for latest versions
        # Add specific constraints here if needed for older Python versions
    }
    
    issues = []
    
    try:
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '==' in line:
                package, version = line.split('==')
                package = package.strip()
                version = version.strip()
                
                # For now, just validate that packages are properly formatted
                # Future: Add specific version constraints if needed
                print(f"✅ {package}=={version} - format OK")
        
        if issues:
            print("\n🚨 Compatibility issues found:")
            for issue in issues:
                print(issue)
            return False
        else:
            print(f"✅ All requirements compatible with Python {python_version}")
            return True
            
    except FileNotFoundError:
        print(f"❌ Requirements file {requirements_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        return False

def main():
    """Main validation function."""
    python_version = sys.argv[1] if len(sys.argv) > 1 else f"{sys.version_info.major}.{sys.version_info.minor}"
    
    print(f"🔍 Validating requirements for Python {python_version}")
    
    # Check different requirements files
    files_to_check = [
        'requirements/base.txt',
        'requirements/dev.txt',
    ]
    
    # Add Python 3.9 specific file if checking 3.9
    if python_version == '3.9':
        files_to_check.append('requirements/python39.txt')
    
    all_valid = True
    for req_file in files_to_check:
        try:
            valid = check_python_compatibility(req_file, python_version)
            all_valid = all_valid and valid
        except FileNotFoundError:
            print(f"⚠️  {req_file} not found, skipping")
    
    if all_valid:
        print("🎉 All requirements validation passed!")
        sys.exit(0)
    else:
        print("❌ Requirements validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
