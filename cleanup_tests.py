#!/usr/bin/env python3
"""
Cleanup script to remove obsolete test files after consolidation.

This script removes the 17 ad-hoc test files from the root directory
and consolidates testing into the proper tests/ directory structure.
"""

import sys
from pathlib import Path

# Files to remove - obsolete ad-hoc tests
OBSOLETE_TEST_FILES = [
    "complete_endpoint_test.py",
    "comprehensive_endpoint_test.py",
    "demo_all_variants.py",
    "test_compat_import.py",
    "test_compat_variants.py",
    "test_compatibility_dry_run.py",
    "test_correct_exception_mapping.py",
    "test_dict_mapping.py",
    "test_error_mapping.py",
    "test_final_improvements.py",
    "test_improved_functions.py",
    "test_proxycurl_compat.py",
    "test_proxycurl_compatibility.py",
    "test_real_proxycurl_compatibility.py",
    "test_specific_variants.py",
    "verify_compat.py",
]

# Test result files to remove
OBSOLETE_RESULT_FILES = [
    "complete_endpoint_test_results.json",
    "endpoint_test_results.json",
    "proxycurl_compat_test_results.json",
]

# Documentation files to remove (now obsolete)
OBSOLETE_DOC_FILES = ["ENDPOINT_TEST_SUMMARY.md", "IMPROVED_EXCEPTION_MAPPING.md"]


def cleanup_files():
    """Remove obsolete test files and consolidate testing."""
    current_dir = Path.cwd()

    print("🧹 CLEANING UP AD-HOC TEST FILES")
    print("=" * 50)

    total_removed = 0
    total_size_saved = 0

    all_files_to_remove = (
        OBSOLETE_TEST_FILES + OBSOLETE_RESULT_FILES + OBSOLETE_DOC_FILES
    )

    for filename in all_files_to_remove:
        file_path = current_dir / filename

        if file_path.exists():
            file_size = file_path.stat().st_size
            total_size_saved += file_size

            file_path.unlink()
            total_removed += 1
            print(f"✅ Removed: {filename} ({file_size:,} bytes)")
        else:
            print(f"⚠️  Not found: {filename}")

    print("\n📊 CLEANUP SUMMARY:")
    print(f"Files removed: {total_removed}")
    print(
        f"Disk space saved: {total_size_saved:,} bytes ({total_size_saved / 1024:.1f} KB)"
    )

    print("\n✅ CONSOLIDATED TEST STRUCTURE:")
    print("tests/")
    print("├── test_enrichlayer.py       # Core library tests")
    print("├── test_compatibility.py     # Formal compatibility tests")
    print("├── test_endpoints.py         # Consolidated endpoint testing")
    print("└── test_exception_mapping.py # Consolidated exception mapping tests")

    print("\n🚀 RUN TESTS WITH:")
    print("cd tests && python -m unittest discover -v")


def confirm_cleanup():
    """Ask user to confirm cleanup operation."""
    print("This will remove 17 obsolete test files from the root directory.")
    print("The functionality is preserved in the consolidated tests/ directory.")
    print()

    response = input("Continue with cleanup? [y/N]: ").lower().strip()
    return response in ["y", "yes"]


def main():
    """Main cleanup function."""
    # Auto-proceed with cleanup
    try:
        cleanup_files()
        print("\n🎉 Test consolidation completed successfully!")
        print("Run the tests to verify everything works:")
        print("python run_tests.py")
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
