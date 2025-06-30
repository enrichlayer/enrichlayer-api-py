"""
EnrichLayer API - Python client for LinkedIn data enrichment.

This package provides a modern, efficient Python client for accessing
LinkedIn profile and company data through the EnrichLayer API.

Basic usage:
    from enrichlayer.asyncio import EnrichLayer
    
    enrichlayer = EnrichLayer()
    person = await enrichlayer.person.get(linkedin_profile_url="...")

Proxycurl compatibility:
    For users migrating from proxycurl-py, enable compatibility mode:
    
    import enrichlayer
    enrichlayer.enable_proxycurl_compatibility()
    
    # Now your existing proxycurl code works unchanged
    from proxycurl.asyncio import Proxycurl
    proxycurl = Proxycurl()
    person = await proxycurl.linkedin.person.get(...)
"""

from .compat import enable_proxycurl_compatibility
from .compat.monkey_patch import ProxycurlException

__version__ = "0.1.0.post2"
__all__ = ['enable_proxycurl_compatibility', 'ProxycurlException']