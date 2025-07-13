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
    
    # Known version constraints for Python 3.9
    python39_constraints = {
        'click': '<8.2.0',  # click 8.2.0+ requires Python 3.10+
        'black': '<24.0.0',  # Some newer black versions require Python 3.10+
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
                
                if package in python39_constraints and python_version == '3.9':
                    constraint = python39_constraints[package]
                    spec = SpecifierSet(constraint)
                    if not spec.contains(version):
                        issues.append(f"❌ {package}=={version} violates Python 3.9 constraint {constraint}")
                    else:
                        print(f"✅ {package}=={version} compatible with Python 3.9")
        
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
