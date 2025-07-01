#!/usr/bin/env python3
"""
Dry run test for proxycurl-py compatibility layer.

This script tests the compatibility layer setup without making actual API calls.
"""

import sys
import traceback


def test_import_and_setup():
    """Test that enrichlayer can be imported and compatibility enabled."""
    print("🧪 Testing enrichlayer import and compatibility setup...")

    try:
        import enrichlayer_client

        print("✅ EnrichLayer imported successfully")

        # Test compatibility function exists
        if hasattr(enrichlayer, "enable_proxycurl_compatibility"):
            print("✅ enable_proxycurl_compatibility function found")
        else:
            print("❌ enable_proxycurl_compatibility function not found")
            return False

        # Enable compatibility (dry run)
        enrichlayer.enable_proxycurl_compatibility(
            api_key="test-key-for-dry-run", deprecation_warnings=False
        )
        print("✅ Compatibility layer enabled successfully")

        return True

    except Exception as e:
        print(f"❌ Failed to setup compatibility: {e}")
        traceback.print_exc()
        return False


def test_wrapper_creation():
    """Test creating proxycurl wrapper classes."""
    print("\n🧪 Testing wrapper class creation...")

    try:
        from enrichlayer_client.asyncio import EnrichLayer
        from enrichlayer_client.compat.monkey_patch import create_proxycurl_wrapper_class

        # Create wrapper class
        ProxycurlWrapper = create_proxycurl_wrapper_class(EnrichLayer)
        print("✅ Wrapper class created successfully")

        # Test instantiation (with mock API key)
        wrapper = ProxycurlWrapper(api_key="test-key")
        print("✅ Wrapper instance created successfully")

        # Test interface
        if hasattr(wrapper, "linkedin"):
            print("✅ linkedin attribute found")
        else:
            print("❌ linkedin attribute not found")
            return False

        if hasattr(wrapper.linkedin, "person"):
            print("✅ linkedin.person attribute found")
        else:
            print("❌ linkedin.person attribute not found")
            return False

        if hasattr(wrapper.linkedin, "company"):
            print("✅ linkedin.company attribute found")
        else:
            print("❌ linkedin.company attribute not found")
            return False

        print("✅ All expected attributes found")
        return True

    except Exception as e:
        print(f"❌ Failed to create wrapper: {e}")
        traceback.print_exc()
        return False


def test_direct_enrichlayer_usage():
    """Test using enrichlayer directly to verify the new API structure."""
    print("\n🧪 Testing direct enrichlayer usage...")

    try:
        from enrichlayer_client.asyncio import EnrichLayer

        # Create instance
        enrichlayer = EnrichLayer(api_key="test-key")
        print("✅ EnrichLayer instance created")

        # Test new direct API structure
        if hasattr(enrichlayer, "person"):
            print("✅ person attribute found")
        else:
            print("❌ person attribute not found")
            return False

        if hasattr(enrichlayer, "company"):
            print("✅ company attribute found")
        else:
            print("❌ company attribute not found")
            return False

        if hasattr(enrichlayer, "school"):
            print("✅ school attribute found")
        else:
            print("❌ school attribute not found")
            return False

        print("✅ New API structure verified")
        return True

    except Exception as e:
        print(f"❌ Failed direct enrichlayer test: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all dry-run tests."""
    print("🔬 Proxycurl-py Compatibility Dry Run Tests")
    print("=" * 60)
    print("Testing compatibility layer setup without API calls")
    print()

    tests = [
        ("Import & Setup", test_import_and_setup),
        ("Wrapper Creation", test_wrapper_creation),
        ("Direct EnrichLayer", test_direct_enrichlayer_usage),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results[test_name] = False

    # Print summary
    print(f"\n{'=' * 60}")
    print("📊 TEST SUMMARY")
    print(f"{'=' * 60}")

    passed = sum(1 for success in results.values() if success)
    total = len(results)

    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n📈 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All dry-run tests passed!")
        print("\n💡 Next Steps:")
        print("   1. Set your ENRICHLAYER_API_KEY environment variable")
        print("   2. Run: python test_proxycurl_compatibility.py")
        print("   3. Test with your actual API to verify full functionality")
    else:
        failed_tests = [name for name, success in results.items() if not success]
        print(f"⚠️  Some tests failed: {', '.join(failed_tests)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
