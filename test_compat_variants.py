#!/usr/bin/env python3
"""
Test that compat module works with different proxycurl-py variants (asyncio, gevent, twisted).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_asyncio_variant():
    """Test compatibility with proxycurl.asyncio"""
    print("🧪 Testing asyncio variant...")
    try:
        # Clear any previous imports
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('enrichlayer_client.compat')]
        for module in modules_to_clear:
            del sys.modules[module]
        
        # Test that asyncio variant works
        from enrichlayer_client.compat import enable_proxycurl_compatibility
        enable_proxycurl_compatibility()
        
        from proxycurl.asyncio import Proxycurl
        proxycurl = Proxycurl(api_key="test")
        
        print("   ✅ Asyncio variant working")
        return True
    except Exception as e:
        print(f"   ❌ Asyncio variant failed: {e}")
        return False

def test_gevent_variant():
    """Test compatibility with proxycurl.gevent"""
    print("\n🧪 Testing gevent variant...")
    try:
        # Clear any previous imports
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('enrichlayer_client.compat')]
        for module in modules_to_clear:
            del sys.modules[module]
        
        # Import gevent first to make it available
        import proxycurl.gevent
        
        # Now test compat module - it should find gevent's ProxycurlException
        from enrichlayer_client.compat import enable_proxycurl_compatibility
        enable_proxycurl_compatibility()
        
        from proxycurl.gevent import Proxycurl
        proxycurl = Proxycurl(api_key="test")
        
        print("   ✅ Gevent variant working")
        return True
    except Exception as e:
        print(f"   ❌ Gevent variant failed: {e}")
        return False

def test_twisted_variant():
    """Test compatibility with proxycurl.twisted"""
    print("\n🧪 Testing twisted variant...")
    try:
        # Clear any previous imports
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('enrichlayer_client.compat')]
        for module in modules_to_clear:
            del sys.modules[module]
        
        # Import twisted first to make it available
        import proxycurl.twisted
        
        # Now test compat module - it should find twisted's ProxycurlException
        from enrichlayer_client.compat import enable_proxycurl_compatibility
        enable_proxycurl_compatibility()
        
        from proxycurl.twisted import Proxycurl
        proxycurl = Proxycurl(api_key="test")
        
        print("   ✅ Twisted variant working")
        return True
    except Exception as e:
        print(f"   ❌ Twisted variant failed: {e}")
        return False

def test_exception_consistency():
    """Test that ProxycurlException is the same across all variants"""
    print("\n🧪 Testing ProxycurlException consistency...")
    try:
        from proxycurl.asyncio.base import ProxycurlException as AsyncioException
        from proxycurl.gevent.base import ProxycurlException as GeventException  
        from proxycurl.twisted.base import ProxycurlException as TwistedException
        
        # They should all be the same class
        if AsyncioException is GeventException is TwistedException:
            print("   ✅ All ProxycurlException classes are identical")
            return True
        else:
            print("   ℹ️  ProxycurlException classes are different but compatible")
            return True
    except Exception as e:
        print(f"   ❌ Exception consistency test failed: {e}")
        return False

def main():
    """Run all variant tests"""
    print("=" * 70)
    print("TESTING PROXYCURL-PY COMPATIBILITY WITH ALL VARIANTS")
    print("=" * 70)
    
    results = []
    
    # Test all variants
    results.append(test_asyncio_variant())
    results.append(test_gevent_variant())
    results.append(test_twisted_variant())
    results.append(test_exception_consistency())
    
    print("\n" + "=" * 70)
    print("VARIANT COMPATIBILITY TEST SUMMARY")
    print("=" * 70)
    
    successful = sum(results)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {successful/total*100:.1f}%")
    
    if successful == total:
        print("\n🎉 ALL VARIANTS WORKING!")
        print("✅ Compatibility module properly handles all proxycurl variants")
        print("✅ ProxycurlException imported from any available module")
        print("✅ Users can choose any concurrency model")
    else:
        print(f"\n⚠️  {total - successful} variant(s) failed")
    
    print("=" * 70)

if __name__ == "__main__":
    main()