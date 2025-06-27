"""
Monkey patching utilities for proxycurl-py compatibility.

This module provides the core functionality to patch the existing proxycurl-py
package to use EnrichLayer backend instead of the original Proxycurl backend.
"""

import os
import sys
import warnings
from typing import Any, Dict, Optional, Type


class LinkedinCompatibilityWrapper:
    """
    Wrapper that provides the linkedin.* interface for compatibility.

    Maps the old proxycurl.linkedin.* structure to the new enrichlayer direct access.
    """

    def __init__(self, enrichlayer_instance: Any) -> None:
        self._enrichlayer = enrichlayer_instance

    @property
    def person(self) -> Any:
        """Provides access to person methods via enrichlayer.person"""
        return self._enrichlayer.person

    @property
    def company(self) -> Any:
        """Provides access to company methods via enrichlayer.company"""
        return self._enrichlayer.company

    @property
    def school(self) -> Any:
        """Provides access to school methods via enrichlayer.school"""
        return self._enrichlayer.school

    @property
    def job(self) -> Any:
        """Provides access to job methods via enrichlayer.job"""
        return self._enrichlayer.job

    @property
    def customers(self) -> Any:
        """Provides access to customers methods via enrichlayer.customers"""
        return self._enrichlayer.customers


def create_proxycurl_wrapper_class(enrichlayer_class: Type[Any]) -> Type[Any]:
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
            init_kwargs: Dict[str, Any] = {"api_key": api_key}
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

        def get_balance(self, **kwargs: Any) -> Any:
            """Maintain compatibility for get_balance method"""
            return super().get_balance(**kwargs)

    return ProxycurlCompatibilityWrapper


def patch_proxycurl_module(
    module_name: str, enrichlayer_class: Type[Any], show_warnings: bool = False
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

    # Import EnrichLayer classes - let source modules handle missing dependencies
    from enrichlayer.asyncio import EnrichLayer as AsyncIOEnrichLayer
    from enrichlayer.gevent import EnrichLayer as GeventEnrichLayer
    from enrichlayer.twisted import EnrichLayer as TwistedEnrichLayer

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
    patch_proxycurl_module("proxycurl.gevent", GeventEnrichLayer, deprecation_warnings)
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

    class ProxycurlImportHook:
        """Import hook that patches proxycurl modules as they're imported"""

        def __init__(self, show_warnings: bool = False):
            self.show_warnings = show_warnings

        def find_spec(self, fullname, path, target=None):
            # We don't need to create a spec, just detect imports
            return None

        def find_module(self, fullname, path=None):
            # Legacy finder for Python < 3.4 compatibility
            return None

    # Install the import hook
    if not any(isinstance(hook, ProxycurlImportHook) for hook in sys.meta_path):
        hook = ProxycurlImportHook(show_warnings)
        sys.meta_path.insert(0, hook)


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
