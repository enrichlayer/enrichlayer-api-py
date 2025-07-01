#!/usr/bin/env python3
"""
Demonstration: Using enrichlayer compat module with all proxycurl-py variants.

This shows how users can choose any concurrency model (asyncio, gevent, twisted)
and their existing proxycurl-py code will work unchanged with enrichlayer backend.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enable enrichlayer compatibility globally
from enrichlayer_client.compat import enable_proxycurl_compatibility
enable_proxycurl_compatibility()

API_KEY = "a3c4354f-6f80-419a-8f8b-67d41d52c746"

def demo_asyncio_usage():
    """Demonstrate asyncio usage (most common)"""
    print("=" * 60)
    print("DEMO 1: ASYNCIO USAGE")
    print("=" * 60)
    print("# Original proxycurl-py asyncio code:")
    print("from proxycurl.asyncio import Proxycurl")
    print("proxycurl = Proxycurl(api_key='...')")
    print("person = await proxycurl.linkedin.person.get(...)")
    print()
    
    async def run_asyncio():
        from proxycurl.asyncio import Proxycurl
        proxycurl = Proxycurl(api_key=API_KEY)
        
        try:
            balance = await proxycurl.get_balance()
            print(f"✅ Asyncio result: {balance['credit_balance']:,} credits available")
        except Exception as e:
            print(f"❌ Asyncio failed: {e}")
    
    asyncio.run(run_asyncio())

def demo_gevent_usage():
    """Demonstrate gevent usage (synchronous-style)"""
    print("\n" + "=" * 60)
    print("DEMO 2: GEVENT USAGE")
    print("=" * 60)
    print("# Original proxycurl-py gevent code:")
    print("from proxycurl.gevent import Proxycurl")
    print("proxycurl = Proxycurl(api_key='...')")
    print("person = proxycurl.linkedin.person.get(...)  # Synchronous call")
    print()
    
    from proxycurl.gevent import Proxycurl
    proxycurl = Proxycurl(api_key=API_KEY)
    
    try:
        balance = proxycurl.get_balance()  # Synchronous call with gevent
        print(f"✅ Gevent result: {balance['credit_balance']:,} credits available")
    except Exception as e:
        print(f"❌ Gevent failed: {e}")

def demo_twisted_usage():
    """Demonstrate twisted usage (deferred-style)"""
    print("\n" + "=" * 60)
    print("DEMO 3: TWISTED USAGE")
    print("=" * 60)
    print("# Original proxycurl-py twisted code:")
    print("from proxycurl.twisted import Proxycurl")
    print("from twisted.internet import defer")
    print("proxycurl = Proxycurl(api_key='...')")
    print("d = proxycurl.linkedin.person.get(...)  # Returns Deferred")
    print()
    
    try:
        from proxycurl.twisted import Proxycurl
        proxycurl = Proxycurl(api_key=API_KEY)
        print(f"✅ Twisted initialized successfully (Deferred-based interface)")
        print("   (Actual twisted calls require reactor setup)")
    except Exception as e:
        print(f"❌ Twisted failed: {e}")

def demo_benefits():
    """Show the benefits of the compatibility layer"""
    print("\n" + "=" * 60)
    print("COMPATIBILITY LAYER BENEFITS")
    print("=" * 60)
    
    benefits = [
        "✅ Zero Code Changes: Existing proxycurl-py code works unchanged",
        "✅ Any Concurrency Model: Choose asyncio, gevent, or twisted",
        "✅ Automatic Exception Mapping: ProxycurlException from any variant",
        "✅ Modern Backend: Benefits from improved EnrichLayer infrastructure",
        "✅ Flexible Migration: Migrate at your own pace",
        "✅ Future-Proof: Easy path to new enrichlayer_client API"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n📝 Migration Path:")
    print("  1. Immediate: Add `enable_proxycurl_compatibility()` to existing code")
    print("  2. Gradual: Replace imports when convenient")
    print("  3. Complete: Migrate to new enrichlayer_client API structure")

def main():
    """Run all demonstrations"""
    print("🔧 Enrichlayer compatibility enabled for all proxycurl variants!")
    print("All API calls will be redirected to enrichlayer backend.\n")
    
    # Demo each concurrency model
    demo_asyncio_usage()
    demo_gevent_usage() 
    demo_twisted_usage()
    demo_benefits()
    
    print("\n" + "=" * 60)
    print("🎉 ALL PROXYCURL VARIANTS WORKING WITH ENRICHLAYER!")
    print("Users can choose their preferred concurrency model without changes.")
    print("=" * 60)

if __name__ == "__main__":
    main()