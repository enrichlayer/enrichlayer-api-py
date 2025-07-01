#!/usr/bin/env python3
"""
Test compat module import without having gevent/twisted installed.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_compat_import_without_optional_deps():
    """Test that compat module can be imported even without gevent/twisted"""
    print("Testing compat module import without optional dependencies...")
    
    try:
        # This should work even if gevent/twisted are not installed
        from enrichlayer_client.compat import enable_proxycurl_compatibility
        print("✅ SUCCESS: compat module imported successfully")
        
        # Test the function call (should work even without optional deps)
        try:
            enable_proxycurl_compatibility()
            print("✅ SUCCESS: enable_proxycurl_compatibility() called successfully")
        except Exception as e:
            print(f"❌ FAILED: enable_proxycurl_compatibility() failed: {e}")
            return False
            
    except ImportError as e:
        if "proxycurl-py" in str(e):
            print(f"✅ SUCCESS: Compat module correctly requires proxycurl-py: {e}")
            return True
        else:
            print(f"❌ FAILED: Unexpected import error: {e}")
            return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        return False
    
    return True

def test_individual_enrichlayer_imports():
    """Test that individual enrichlayer modules work correctly"""
    print("\nTesting individual enrichlayer module imports...")
    
    # Test asyncio (should always work)
    try:
        from enrichlayer_client.asyncio import EnrichLayer
        print("✅ SUCCESS: asyncio EnrichLayer imported")
    except Exception as e:
        print(f"❌ FAILED: asyncio EnrichLayer import failed: {e}")
        return False
    
    # Test gevent (should fail gracefully if not installed)
    try:
        from enrichlayer_client.gevent import EnrichLayer as GeventEnrichLayer
        print("✅ SUCCESS: gevent EnrichLayer imported (gevent is installed)")
    except ImportError as e:
        print(f"ℹ️  INFO: gevent EnrichLayer not available (expected if gevent not installed): {e}")
    except Exception as e:
        print(f"❌ FAILED: Unexpected error importing gevent EnrichLayer: {e}")
        return False
    
    # Test twisted (should fail gracefully if not installed)
    try:
        from enrichlayer_client.twisted import EnrichLayer as TwistedEnrichLayer
        print("✅ SUCCESS: twisted EnrichLayer imported (twisted is installed)")
    except ImportError as e:
        print(f"ℹ️  INFO: twisted EnrichLayer not available (expected if twisted not installed): {e}")
    except Exception as e:
        print(f"❌ FAILED: Unexpected error importing twisted EnrichLayer: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("TESTING COMPAT MODULE OPTIONAL DEPENDENCY HANDLING")
    print("=" * 60)
    
    success1 = test_compat_import_without_optional_deps()
    success2 = test_individual_enrichlayer_imports()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED: Compat module handles optional dependencies correctly")
    else:
        print("❌ SOME TESTS FAILED: Compat module needs fixes")
    print("=" * 60)

if __name__ == "__main__":
    main()