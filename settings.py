"""
Settings module for managing Azure OpenAI API configuration.
"""

import os
import json


class Settings:
    """Manages application settings, particularly Azure OpenAI API configuration."""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".educontent")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self._ensure_config_dir()
        self.config = self._load_config()
    
    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def _load_config(self):
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get_config(self):
        """Get the entire configuration dictionary."""
        return self.config.copy()
    
    def set_config(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
        return self._save_config()
    
    def get_value(self, key, default=None):
        """Get a specific configuration value."""
        return self.config.get(key, default)
    
    def is_configured(self):
        """Check if Azure OpenAI is properly configured."""
        required_keys = ['endpoint', 'api_key', 'deployment']
        return all(key in self.config and self.config[key] for key in required_keys)
    
    def clear_config(self):
        """Clear all configuration."""
        self.config = {}
        return self._save_config()
    
    def get_azure_config(self):
        """Get Azure OpenAI configuration for API calls."""
        return {
            'endpoint': self.config.get('endpoint'),
            'api_key': self.config.get('api_key'),
            'deployment': self.config.get('deployment'),
            'api_version': self.config.get('api_version', '2024-02-15-preview')
        }
