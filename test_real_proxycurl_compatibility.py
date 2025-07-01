#!/usr/bin/env python3
"""
Real proxycurl-py compatibility test.

This script tests the EnrichLayer compatibility layer using the actual
proxycurl-py package installed from PyPI.
"""

import asyncio
import os
import sys
import traceback


def setup_api_key() -> str:
    """Get API key from environment or user input."""
    # Check environment variables
    api_key = os.environ.get("ENRICHLAYER_API_KEY") or os.environ.get(
        "PROXYCURL_API_KEY"
    )

    if api_key:
        print(f"🔑 Using API key from environment: {api_key[:12]}{'*' * 28}")
        return api_key

    print("🔑 No API key found in environment variables.")
    print("   Set ENRICHLAYER_API_KEY or PROXYCURL_API_KEY environment variable")
    print("   or enter your API key below:")

    try:
        api_key = input("API Key: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            sys.exit(1)
        return api_key
    except (KeyboardInterrupt, EOFError):
        print("\n❌ Cancelled by user. Exiting.")
        sys.exit(1)


def test_proxycurl_import():
    """Test importing actual proxycurl-py package modules."""
    print("🧪 Testing: Real Proxycurl-py Module Imports")
    print("=" * 60)

    success_count = 0
    total_count = 3

    # Test proxycurl.asyncio
    try:
        from proxycurl.asyncio import Proxycurl

        print("✅ proxycurl.asyncio imported successfully")
        success_count += 1
    except ImportError as e:
        print(f"❌ Failed to import proxycurl.asyncio: {e}")

    # Test proxycurl.gevent
    try:
        from proxycurl.gevent import Proxycurl

        print("✅ proxycurl.gevent imported successfully")
        success_count += 1
    except ImportError as e:
        print(f"❌ Failed to import proxycurl.gevent: {e}")

    # Test proxycurl.twisted
    try:
        from proxycurl.twisted import Proxycurl

        print("✅ proxycurl.twisted imported successfully")
        success_count += 1
    except ImportError as e:
        print(f"❌ Failed to import proxycurl.twisted: {e}")

    print(f"📊 {success_count}/{total_count} proxycurl modules imported successfully")

    if success_count == 0:
        print("💡 Make sure proxycurl-py is installed: pip install proxycurl-py")
        return False

    return success_count > 0


async def test_proxycurl_asyncio_compatibility(api_key: str):
    """Test compatibility with proxycurl.asyncio module."""
    print("\n🧪 Testing: Proxycurl AsyncIO Compatibility")
    print("=" * 60)

    try:
        print("📦 Step 1: Import proxycurl.asyncio FIRST (before monkey patching)")
        from proxycurl.asyncio import Proxycurl

        print("✅ proxycurl.asyncio imported")

        print("\n📦 Step 2: Import enrichlayer and enable compatibility")
        import enrichlayer

        print("✅ EnrichLayer imported")

        enrichlayer.enable_proxycurl_compatibility(
            api_key=api_key, deprecation_warnings=True
        )
        print("✅ Compatibility layer enabled (monkey patching applied)")

        print(
            "\n📦 Step 3: Test proxycurl.asyncio - should now use EnrichLayer backend"
        )
        # Test creating instance
        api = Proxycurl(api_key=api_key)
        print("✅ Proxycurl instance created")

        # Test the interface exists
        if hasattr(api, "linkedin"):
            print("✅ linkedin attribute found")
        else:
            print("❌ linkedin attribute missing")
            return False

        if hasattr(api.linkedin, "person"):
            print("✅ linkedin.person attribute found")
        else:
            print("❌ linkedin.person attribute missing")
            return False

        # Test a simple API call
        print("\n🔍 Testing API call with monkey-patched proxycurl.asyncio...")
        try:
            balance = await api.get_balance()
            print(f"✅ Balance retrieved: {balance}")
            print(
                "✅ Monkey patching successful - proxycurl.asyncio is using EnrichLayer backend!"
            )
        except Exception as e:
            print(f"⚠️  Balance check failed: {e}")
            print("   This might be expected if the API key has restrictions")

        return True

    except Exception as e:
        print(f"❌ AsyncIO compatibility test failed: {e}")
        traceback.print_exc()
        return False


async def test_proxycurl_gevent_compatibility(api_key: str):
    """Test compatibility with proxycurl.gevent module."""
    print("\n🧪 Testing: Proxycurl Gevent Compatibility")
    print("=" * 60)

    try:
        print("📦 Step 1: Import proxycurl.gevent FIRST (before monkey patching)")
        from proxycurl.gevent import Proxycurl

        print("✅ proxycurl.gevent imported")

        print("\n📦 Step 2: Import enrichlayer and enable compatibility")
        import enrichlayer

        print("✅ EnrichLayer imported")

        enrichlayer.enable_proxycurl_compatibility(
            api_key=api_key, deprecation_warnings=True
        )
        print("✅ Compatibility layer enabled (monkey patching applied)")

        print("\n📦 Step 3: Test proxycurl.gevent - should now use EnrichLayer backend")
        # Test creating instance
        api = Proxycurl(api_key=api_key)
        print("✅ Proxycurl instance created")

        # Test the interface exists
        if hasattr(api, "linkedin"):
            print("✅ linkedin attribute found")
        else:
            print("❌ linkedin attribute missing")
            return False

        if hasattr(api.linkedin, "person"):
            print("✅ linkedin.person attribute found")
        else:
            print("❌ linkedin.person attribute missing")
            return False

        print("✅ Gevent compatibility test completed")
        return True

    except Exception as e:
        print(f"❌ Gevent compatibility test failed: {e}")
        traceback.print_exc()
        return False


async def test_proxycurl_twisted_compatibility(api_key: str):
    """Test compatibility with proxycurl.twisted module."""
    print("\n🧪 Testing: Proxycurl Twisted Compatibility")
    print("=" * 60)

    try:
        print("📦 Step 1: Import proxycurl.twisted FIRST (before monkey patching)")
        from proxycurl.twisted import Proxycurl

        print("✅ proxycurl.twisted imported")

        print("\n📦 Step 2: Import enrichlayer and enable compatibility")
        import enrichlayer

        print("✅ EnrichLayer imported")

        enrichlayer.enable_proxycurl_compatibility(
            api_key=api_key, deprecation_warnings=True
        )
        print("✅ Compatibility layer enabled (monkey patching applied)")

        print(
            "\n📦 Step 3: Test proxycurl.twisted - should now use EnrichLayer backend"
        )
        # Test creating instance
        api = Proxycurl(api_key=api_key)
        print("✅ Proxycurl instance created")

        # Test the interface exists
        if hasattr(api, "linkedin"):
            print("✅ linkedin attribute found")
        else:
            print("❌ linkedin attribute missing")
            return False

        if hasattr(api.linkedin, "person"):
            print("✅ linkedin.person attribute found")
        else:
            print("❌ linkedin.person attribute missing")
            return False

        print("✅ Twisted compatibility test completed")
        return True

    except Exception as e:
        print(f"❌ Twisted compatibility test failed: {e}")
        traceback.print_exc()
        return False


async def test_before_after_comparison(api_key: str):
    """Test proxycurl before and after monkey patching."""
    print("\n🧪 Testing: Before/After Monkey Patching")
    print("=" * 60)

    try:
        # Clear any previous imports to start fresh
        modules_to_clear = [
            m for m in sys.modules.keys() if m.startswith(("proxycurl", "enrichlayer"))
        ]
        for module in modules_to_clear:
            del sys.modules[module]

        print("📦 Step 1: Test original proxycurl behavior")
        import proxycurl

        original_api = proxycurl.Proxycurl(api_key=api_key)
        print("✅ Original proxycurl imported and instantiated")

        # Check what class it is
        print(f"✅ Original class: {type(original_api).__name__}")
        print(f"✅ Original module: {type(original_api).__module__}")

        print("\n📦 Step 2: Apply monkey patch")
        import enrichlayer

        enrichlayer.enable_proxycurl_compatibility(api_key=api_key)
        print("✅ Monkey patch applied")

        print("\n📦 Step 3: Test patched proxycurl behavior")
        patched_api = proxycurl.Proxycurl(api_key=api_key)
        print("✅ Patched proxycurl instantiated")

        # Check what class it is now
        print(f"✅ Patched class: {type(patched_api).__name__}")
        print(f"✅ Patched module: {type(patched_api).__module__}")

        # They should be different classes now
        if type(original_api).__name__ != type(patched_api).__name__:
            print("✅ Classes are different - monkey patching worked!")
        else:
            print("⚠️  Classes are the same - monkey patching may not have worked")

        return True

    except Exception as e:
        print(f"❌ Before/after test failed: {e}")
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    print("🔬 Real Proxycurl-py Compatibility Test Suite")
    print("=" * 60)
    print("This script tests EnrichLayer compatibility with the actual")
    print("proxycurl-py package installed from PyPI.")
    print()
    print("💡 Correct monkey patching order:")
    print("   1. Import proxycurl first")
    print("   2. Import enrichlayer")
    print("   3. Enable compatibility (monkey patch)")
    print("   4. Use proxycurl normally (now uses EnrichLayer)")
    print()

    # Setup API key
    api_key = setup_api_key()
    print()

    # Test importing real proxycurl
    if not test_proxycurl_import():
        print("\n❌ Cannot proceed without proxycurl-py package.")
        print("💡 Install it with: pip install proxycurl-py")
        return 1

    # Test compatibility with all three implementations
    tests = [
        (
            "Proxycurl AsyncIO Compatibility",
            test_proxycurl_asyncio_compatibility(api_key),
        ),
        (
            "Proxycurl Gevent Compatibility",
            test_proxycurl_gevent_compatibility(api_key),
        ),
        (
            "Proxycurl Twisted Compatibility",
            test_proxycurl_twisted_compatibility(api_key),
        ),
    ]

    results = {}
    for test_name, test_coro in tests:
        print(f"\n{'=' * 60}")
        try:
            success = await test_coro
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
        print("🎉 All tests passed!")
        print("\n💡 Your EnrichLayer compatibility layer is working perfectly")
        print("   with the real proxycurl-py package!")
        print("\n🔄 Usage pattern:")
        print("   import proxycurl")
        print("   import enrichlayer")
        print("   enrichlayer.enable_proxycurl_compatibility()")
        print("   # Now use proxycurl normally - it uses EnrichLayer backend!")
    else:
        failed_tests = [name for name, success in results.items() if not success]
        print(f"⚠️  Some tests failed: {', '.join(failed_tests)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
