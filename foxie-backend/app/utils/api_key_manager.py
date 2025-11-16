"""
API Key Management Utility for Foxie Platform.
Handles Google Gemini API key validation and retrieval from multiple sources.
"""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class APIKeyManager:
    """Manages Google Gemini API key from multiple sources with priority."""
    
    ENV_VAR_NAME = "GOOGLE_API_KEY"
    
    @classmethod
    def get_api_key(
        cls,
        provided_key: Optional[str] = None,
        raise_if_missing: bool = True
    ) -> Optional[str]:
        """
        Get Google Gemini API key from multiple sources with priority:
        1. Explicitly provided key (highest priority)
        2. Environment variable GOOGLE_API_KEY
        3. .env file in current directory
        4. .env file in user's home directory
        
        Args:
            provided_key: Explicitly provided API key
            raise_if_missing: If True, raises ValueError when no key is found
            
        Returns:
            API key string or None if not found
            
        Raises:
            ValueError: If raise_if_missing=True and no key is found
        """
        # Priority 1: Explicitly provided
        if provided_key:
            if cls._validate_key_format(provided_key):
                return provided_key
            else:
                raise ValueError("Invalid API key format provided")
        
        # Priority 2: Environment variable
        env_key = os.getenv(cls.ENV_VAR_NAME)
        if env_key:
            if cls._validate_key_format(env_key):
                return env_key
        
        # Priority 3: .env in current directory (already loaded by load_dotenv())
        
        # Priority 4: .env in home directory
        home_env = Path.home() / ".foxie" / ".env"
        if home_env.exists():
            from dotenv import dotenv_values
            config = dotenv_values(home_env)
            home_key = config.get(cls.ENV_VAR_NAME)
            if home_key and cls._validate_key_format(home_key):
                return home_key
        
        # No key found
        if raise_if_missing:
            raise ValueError(
                f"Google Gemini API key not found. Please provide it via:\n"
                f"1. Explicitly pass it to the function\n"
                f"2. Set {cls.ENV_VAR_NAME} environment variable\n"
                f"3. Create .env file with {cls.ENV_VAR_NAME}=your_key\n"
                f"4. Create ~/.foxie/.env with {cls.ENV_VAR_NAME}=your_key"
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
    def save_api_key_to_config(cls, api_key: str) -> Path:
        """
        Save API key to user's home directory config file.
        Creates ~/.foxie/.env if it doesn't exist.
        
        Args:
            api_key: API key to save
            
        Returns:
            Path to the saved config file
        """
        if not cls._validate_key_format(api_key):
            raise ValueError("Invalid API key format")
        
        config_dir = Path.home() / ".foxie"
        config_dir.mkdir(exist_ok=True)
        
        env_file = config_dir / ".env"
        
        # Read existing content if file exists
        existing_content = {}
        if env_file.exists():
            from dotenv import dotenv_values
            existing_content = dotenv_values(env_file)
        
        # Update with new key
        existing_content[cls.ENV_VAR_NAME] = api_key
        
        # Write back
        with open(env_file, "w") as f:
            for key, value in existing_content.items():
                f.write(f"{key}={value}\n")
        
        return env_file
    
    @classmethod
    def check_api_key_exists(cls) -> bool:
        """Check if an API key is configured anywhere."""
        try:
            cls.get_api_key(raise_if_missing=False)
            return True
        except:
            return False
