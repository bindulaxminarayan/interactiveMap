#!/usr/bin/env python3
"""
Simple script to run UI tests with common configurations.
"""
import subprocess
import sys
import os

def main():
    """Run UI tests with different configurations."""
    
    # Change to the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    os.chdir(project_root)
    
    print("🧪 Interactive Map UI Tests Runner")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage:")
        print("  python tests/uitests/run_tests.py [options]")
        print("")
        print("Options:")
        print("  --help          Show this help message")
        print("  --headful       Run tests with visible browser")
        print("  --verbose       Run tests with verbose output")
        print("  --category      Run only category validation tests")
        print("  --debug         Run with debug logging")
        print("  --report        Generate HTML report")
        print("")
        print("Examples:")
        print("  python tests/uitests/run_tests.py")
        print("  python tests/uitests/run_tests.py --headful --verbose")
        print("  python tests/uitests/run_tests.py --category --report")
        return
    
    # Build pytest command
    cmd = ["pytest", "tests/uitests/"]
    
    # Parse arguments
    if "--headful" in sys.argv:
        print("🔍 Running with visible browser")
        # Note: headful mode requires modifying conftest.py
        cmd.append("-s")
    
    if "--verbose" in sys.argv:
        print("📝 Running with verbose output")
        cmd.extend(["-v", "-s"])
    
    if "--category" in sys.argv:
        print("📂 Running only category validation tests")
        cmd = ["pytest", "tests/uitests/test_category_validation.py"]
    
    if "--debug" in sys.argv:
        print("🐛 Running with debug logging")
        cmd.append("--log-cli-level=DEBUG")
    
    if "--report" in sys.argv:
        print("📊 Will generate HTML report")
        os.makedirs("test-reports", exist_ok=True)
        cmd.extend([
            "--html=test-reports/ui-tests.html",
            "--self-contained-html"
        ])
    
    # Default verbose if no specific options
    if len(sys.argv) == 1:
        cmd.extend(["-v"])
    
    print(f"🚀 Running command: {' '.join(cmd)}")
    print("-" * 40)
    
    try:
        # Check if dependencies are installed
        result = subprocess.run(
            ["python", "-c", "import playwright; import pytest"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Missing dependencies! Please install them first:")
            print("   Option 1: pip install -e \".[test]\"")
            print("   Option 2 (if package discovery errors): pip install pytest>=7.0.0 pytest-playwright>=0.4.0 playwright>=1.40.0 pytest-asyncio>=0.21.0")
            print("   Then: playwright install chromium")
            return 1
        
        # Run the tests
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            if "--report" in sys.argv:
                print("📊 HTML report generated: test-reports/ui-tests.html")
        else:
            print("❌ Some tests failed!")
            if "--report" in sys.argv:
                print("📊 HTML report with failures: test-reports/ui-tests.html")
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install test dependencies:")
        print("   pip install -e \".[test]\"")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1

if __name__ == "__main__":
    exit(main())
