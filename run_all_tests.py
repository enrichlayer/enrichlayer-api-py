#!/usr/bin/env python3
"""
Run all consolidated tests and generate comprehensive reports.
"""

import subprocess
import sys
import os


def run_all_tests():
    """Run all test suites with consolidated endpoint testing."""
    
    # Set API key if not already set
    if not os.environ.get('ENRICHLAYER_API_KEY'):
        os.environ['ENRICHLAYER_API_KEY'] = 'a3c4354f-6f80-419a-8f8b-67d41d52c746'
    
    print("🧪 RUNNING CONSOLIDATED TEST SUITE")
    print("=" * 60)
    
    test_files = [
        "tests/test_enrichlayer.py",
        "tests/test_exception_mapping.py", 
        "tests/test_endpoints.py",
        "tests/test_compatibility.py"
    ]
    
    success_count = 0
    total_count = len(test_files)
    
    for test_file in test_files:
        print(f"\n🔍 Running {test_file}...")
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', test_file, '-v'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {test_file} - PASSED")
                success_count += 1
            else:
                print(f"❌ {test_file} - FAILED")
                print("STDERR:", result.stderr[:500])
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_file} - TIMEOUT")
        except Exception as e:
            print(f"💥 {test_file} - ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"TEST SUITE SUMMARY")
    print(f"{'='*60}")
    print(f"Total Test Files: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    print(f"Success Rate: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 ALL TESTS PASSED!")
        print("📁 Check tests/ directory for detailed reports:")
        print("   • tests/equal_coverage_test_report.json")
        print("   • tests/equal_coverage_summary.txt") 
        print("   • tests/executive_summary.json")
    else:
        print(f"\n⚠️  {total_count - success_count} test file(s) failed")
        
    return success_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)