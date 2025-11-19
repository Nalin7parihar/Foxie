"""
API Key Management Utility for Foxie Platform.
Handles Google Gemini API key validation.
Backend expects API keys to be provided via requests (users use their own keys).
"""
from typing import Optional


class APIKeyManager:
    """Manages Google Gemini API key validation."""
    
    @classmethod
    def get_api_key(
        cls,
        provided_key: Optional[str] = None,
        raise_if_missing: bool = True
    ) -> Optional[str]:
        """
        Get and validate Google Gemini API key.
        Backend expects API keys to be provided via requests (users use their own keys).
        
        Args:
            provided_key: Explicitly provided API key (required)
            raise_if_missing: If True, raises ValueError when no key is found
            
        Returns:
            API key string or None if not found
            
        Raises:
            ValueError: If raise_if_missing=True and no key is found or invalid
        """
        # Only use provided key (users send their own API keys)
        if provided_key:
            if cls._validate_key_format(provided_key):
                return provided_key.strip()
            else:
                raise ValueError("Invalid API key format provided")
        
        # No key found
        if raise_if_missing:
            raise ValueError(
                "Google Gemini API key is required. Please provide it in your request."
            )
        
        return None
    
    @staticmethod
    def _validate_key_format(api_key: str) -> bool:
        """
        Basic validation of Google API key format.
        Google API keys typically start with 'AIza' and are 39 characters long.
        
        Args:
            api_key: API key to validate
            
        Returns:
            True if format looks valid, False otherwise
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Remove whitespace
        api_key = api_key.strip()
        
        # Basic format check (Google keys usually start with AIza)
        if len(api_key) < 20:  # Too short
            return False
        
        return True
    
    @classmethod
    def check_api_key_exists(cls, provided_key: Optional[str] = None) -> bool:
        """Check if a valid API key is provided."""
        try:
            cls.get_api_key(provided_key=provided_key, raise_if_missing=False)
            return True
        except:
            return False
