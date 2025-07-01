"""
Monkey patching utilities for proxycurl-py compatibility.

This module provides the core functionality to patch the existing proxycurl-py
package to use EnrichLayer backend instead of the original Proxycurl backend.
"""

from __future__ import annotations

import os
import sys
import warnings
import functools
import asyncio
from typing import Any, Optional


# Import ProxycurlException from proxycurl-py (required for compatibility module)
try:
    from proxycurl.base import ProxycurlException
except ImportError:
    raise ImportError(
        "The compatibility module requires proxycurl-py to be installed. "
        "Install it with: pip install proxycurl-py"
    ) from None


def error_mapping_decorator(func: Any) -> Any:
    """
    Decorator that catches EnrichLayerException and re-raises as ProxycurlException.

    This ensures that users of the compatibility layer see proxycurl-style errors
    instead of enrichlayer-specific errors.
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Import here to avoid circular imports
            from enrichlayer_client.asyncio.base import (
                EnrichLayerException as AsyncEnrichLayerException,
            )

            # Try to import gevent implementation
            try:
                from enrichlayer_client.gevent.base import (
                    EnrichLayerException as GeventEnrichLayerException,
                )
            except ImportError:
                GeventEnrichLayerException = None  # type: ignore

            # Try to import twisted implementation
            try:
                from enrichlayer_client.twisted.base import (
                    EnrichLayerException as TwistedEnrichLayerException,
                )
            except ImportError:
                TwistedEnrichLayerException = None  # type: ignore

            # Check if this is an EnrichLayer exception from any implementation
            exception_types = [AsyncEnrichLayerException]
            if GeventEnrichLayerException is not None:
                exception_types.append(GeventEnrichLayerException)  # type: ignore
            if TwistedEnrichLayerException is not None:
                exception_types.append(TwistedEnrichLayerException)  # type: ignore
            
            if isinstance(e, tuple(exception_types)):
                # Re-raise as ProxycurlException with the same message and context
                raise ProxycurlException(str(e)) from e
            else:
                # Re-raise other exceptions unchanged
                raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Import here to avoid circular imports
            # Try to import gevent implementation
            try:
                from enrichlayer_client.gevent.base import (
                    EnrichLayerException as GeventEnrichLayerException,
                )
            except ImportError:
                GeventEnrichLayerException = None  # type: ignore

            # Try to import twisted implementation
            try:
                from enrichlayer_client.twisted.base import (
                    EnrichLayerException as TwistedEnrichLayerException,
                )
            except ImportError:
                TwistedEnrichLayerException = None  # type: ignore

            # Check if this is an EnrichLayer exception from any implementation
            exception_types = []
            if GeventEnrichLayerException is not None:
                exception_types.append(GeventEnrichLayerException)  # type: ignore
            if TwistedEnrichLayerException is not None:
                exception_types.append(TwistedEnrichLayerException)  # type: ignore
            
            if exception_types and isinstance(e, tuple(exception_types)):
                # Re-raise as ProxycurlException with the same message and context
                raise ProxycurlException(str(e)) from e
            else:
                # Re-raise other exceptions unchanged
                raise

    # Return appropriate wrapper based on whether the function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


class ErrorMappingWrapper:
    """
    Wrapper that applies error mapping to all methods of an object.

    This ensures that all method calls from the wrapped object get proper
    error mapping from EnrichLayerException to ProxycurlException.
    """

    def __init__(self, wrapped_object: Any) -> None:
        self._wrapped = wrapped_object

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._wrapped, name)
        if callable(attr):
            return error_mapping_decorator(attr)
        return attr


class LinkedinCompatibilityWrapper:
    """
    Wrapper that provides the linkedin.* interface for compatibility.

    Maps the old proxycurl.linkedin.* structure to the new enrichlayer direct access.
    """

    def __init__(self, enrichlayer_instance: Any) -> None:
        self._enrichlayer = enrichlayer_instance

    @property
    def person(self) -> Any:
        """Provides access to person methods via enrichlayer.person with error mapping"""
        return ErrorMappingWrapper(self._enrichlayer.person)

    @property
    def company(self) -> Any:
        """Provides access to company methods via enrichlayer.company with error mapping"""
        return ErrorMappingWrapper(self._enrichlayer.company)

    @property
    def school(self) -> Any:
        """Provides access to school methods via enrichlayer.school with error mapping"""
        return ErrorMappingWrapper(self._enrichlayer.school)

    @property
    def job(self) -> Any:
        """Provides access to job methods via enrichlayer.job with error mapping"""
        return ErrorMappingWrapper(self._enrichlayer.job)

    @property
    def customers(self) -> Any:
        """Provides access to customers methods via enrichlayer.customers with error mapping"""
        return ErrorMappingWrapper(self._enrichlayer.customers)


def create_proxycurl_wrapper_class(enrichlayer_class: type[Any]) -> type[Any]:
    """
    Creates a Proxycurl wrapper class that uses EnrichLayer backend.

    Args:
        enrichlayer_class: The EnrichLayer class to wrap (AsyncIO, Gevent, or Twisted)

    Returns:
        A class that mimics the original Proxycurl interface
    """

    class ProxycurlCompatibilityWrapper(enrichlayer_class):
        """
        Proxycurl compatibility wrapper that delegates to EnrichLayer.

        This class maintains the exact same interface as the original Proxycurl
        class but uses EnrichLayer backend for all operations.
        """

        def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout: Optional[int] = None,
            max_retries: Optional[int] = None,
            max_backoff_seconds: Optional[int] = None,
            **kwargs: Any,
        ) -> None:
            # Handle legacy PROXYCURL_API_KEY environment variable
            if api_key is None:
                api_key = os.environ.get("PROXYCURL_API_KEY") or os.environ.get(
                    "ENRICHLAYER_API_KEY", ""
                )

            # Initialize the EnrichLayer backend with only non-None values
            init_kwargs: dict[str, Any] = {"api_key": api_key}
            if base_url is not None:
                init_kwargs["base_url"] = base_url
            if timeout is not None:
                init_kwargs["timeout"] = timeout
            if max_retries is not None:
                init_kwargs["max_retries"] = max_retries
            if max_backoff_seconds is not None:
                init_kwargs["max_backoff_seconds"] = max_backoff_seconds
            init_kwargs.update(kwargs)

            super().__init__(**init_kwargs)

            # Store reference for method delegation
            self.enrichlayer = self

            # Create the linkedin compatibility wrapper
            self.linkedin = LinkedinCompatibilityWrapper(self)

        @error_mapping_decorator
        def get_balance(self, **kwargs: Any) -> Any:
            """Maintain compatibility for get_balance method with error mapping"""
            return super().get_balance(**kwargs)

    return ProxycurlCompatibilityWrapper


def patch_proxycurl_module(
    module_name: str, enrichlayer_class: type[Any], show_warnings: bool = False
) -> None:
    """
    Patch a specific proxycurl module to use EnrichLayer backend.

    Args:
        module_name: Name of the module to patch (e.g., 'proxycurl.asyncio')
        enrichlayer_class: The EnrichLayer class to use as backend
        show_warnings: Whether to show deprecation warnings
    """

    if module_name not in sys.modules:
        # Module not imported yet, nothing to patch
        return

    module = sys.modules[module_name]

    if not hasattr(module, "Proxycurl"):
        # Module doesn't have Proxycurl class, nothing to patch
        return

    # Store original class for reference
    if not hasattr(module, "_original_Proxycurl"):
        setattr(module, "_original_Proxycurl", getattr(module, "Proxycurl"))

    # Replace with compatibility wrapper
    setattr(module, "Proxycurl", create_proxycurl_wrapper_class(enrichlayer_class))

    if show_warnings:
        warnings.warn(
            f"Module {module_name} has been patched to use EnrichLayer backend. "
            "Consider migrating to enrichlayer-api for future-proof code.",
            FutureWarning,
            stacklevel=3,
        )


def enable_proxycurl_compatibility(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    deprecation_warnings: bool = False,
) -> None:
    """
    Enable proxycurl-py compatibility by monkey patching existing proxycurl modules.

    This function patches the proxycurl-py package (if installed and imported) to use
    the EnrichLayer backend instead of the original Proxycurl backend. This allows
    existing code using proxycurl-py to work unchanged while benefiting from the
    new EnrichLayer infrastructure.

    Args:
        api_key: Default API key to use for EnrichLayer (overrides environment variables)
        base_url: Default base URL to use for EnrichLayer
        deprecation_warnings: Whether to show warnings about deprecated proxycurl usage

    Example:
        import enrichlayer
        enrichlayer.enable_proxycurl_compatibility()

        # Now existing proxycurl code works with EnrichLayer backend
        from proxycurl.asyncio import Proxycurl
        proxycurl = Proxycurl()
        person = proxycurl.linkedin.person.get(linkedin_profile_url="...")

    Note:
        This function should be called before importing any proxycurl modules,
        or after importing them but before creating Proxycurl instances.
    """

    # Import EnrichLayer classes - handle missing dependencies gracefully
    from enrichlayer_client.asyncio import EnrichLayer as AsyncIOEnrichLayer
    
    try:
        from enrichlayer_client.gevent import EnrichLayer as GeventEnrichLayer
    except ImportError:
        GeventEnrichLayer = None  # type: ignore
    
    try:
        from enrichlayer_client.twisted import EnrichLayer as TwistedEnrichLayer
    except ImportError:
        TwistedEnrichLayer = None  # type: ignore

    # Set default configuration if provided
    if api_key is not None:
        os.environ["ENRICHLAYER_API_KEY"] = api_key
        # Also set PROXYCURL_API_KEY for compatibility
        os.environ["PROXYCURL_API_KEY"] = api_key

    if base_url is not None:
        os.environ["BASE_URL"] = base_url

    # Patch all proxycurl modules that might be loaded
    patch_proxycurl_module(
        "proxycurl.asyncio", AsyncIOEnrichLayer, deprecation_warnings
    )
    if GeventEnrichLayer is not None:
        patch_proxycurl_module("proxycurl.gevent", GeventEnrichLayer, deprecation_warnings)
    if TwistedEnrichLayer is not None:
        patch_proxycurl_module(
            "proxycurl.twisted", TwistedEnrichLayer, deprecation_warnings
        )

    # Set up import hooks for future imports
    _setup_import_hooks(deprecation_warnings)


def _setup_import_hooks(show_warnings: bool = False) -> None:
    """
    Set up import hooks to automatically patch proxycurl modules when they're imported.

    This ensures that even if proxycurl modules are imported after calling
    enable_proxycurl_compatibility(), they will still be patched.
    """

    # Store original __import__ to call later
    original_import = (
        __builtins__["__import__"]
        if isinstance(__builtins__, dict)
        else __builtins__.__import__
    )

    def patching_import(name, globals=None, locals=None, fromlist=(), level=0):
        """Custom import function that patches proxycurl modules after they're imported."""

        # Call the original import first
        module = original_import(name, globals, locals, fromlist, level)

        # Check if we imported a proxycurl module that needs patching
        if name.startswith("proxycurl."):
            # Import EnrichLayer classes for patching - handle missing dependencies
            from enrichlayer_client.asyncio import EnrichLayer as AsyncIOEnrichLayer
            
            try:
                from enrichlayer_client.gevent import EnrichLayer as GeventEnrichLayer
            except ImportError:
                GeventEnrichLayer = None  # type: ignore
            
            try:
                from enrichlayer_client.twisted import EnrichLayer as TwistedEnrichLayer
            except ImportError:
                TwistedEnrichLayer = None  # type: ignore

            if name == "proxycurl.asyncio":
                patch_proxycurl_module(name, AsyncIOEnrichLayer, show_warnings)
            elif name == "proxycurl.gevent" and GeventEnrichLayer is not None:
                patch_proxycurl_module(name, GeventEnrichLayer, show_warnings)
            elif name == "proxycurl.twisted" and TwistedEnrichLayer is not None:
                patch_proxycurl_module(name, TwistedEnrichLayer, show_warnings)

        return module

    # Replace the built-in __import__ function
    if isinstance(__builtins__, dict):
        __builtins__["__import__"] = patching_import
    else:
        __builtins__.__import__ = patching_import


def disable_proxycurl_compatibility():
    """
    Disable proxycurl compatibility and restore original Proxycurl classes.

    This function restores the original Proxycurl classes in all loaded
    proxycurl modules, effectively disabling the EnrichLayer backend.
    """

    modules_to_restore = ["proxycurl.asyncio", "proxycurl.gevent", "proxycurl.twisted"]

    for module_name in modules_to_restore:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            if hasattr(module, "_original_Proxycurl"):
                setattr(module, "Proxycurl", getattr(module, "_original_Proxycurl"))
                delattr(module, "_original_Proxycurl")

    # Remove import hooks
    sys.meta_path = [
        hook
        for hook in sys.meta_path
        if not (
            hasattr(hook, "__class__")
            and getattr(hook.__class__, "__name__", "") == "ProxycurlImportHook"
        )
    ]
