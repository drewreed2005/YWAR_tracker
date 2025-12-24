"""
config.py
---------
Centralized configuration loader.

Responsibilities:
- Loading default.yaml (always required)
- Loading user.yaml (optional override)
- Merging them so user settings override defaults
- Exposing a single CONFIG dictionary for the rest of the app

By doing so, I am keeping configuration logic and magic numbers out of UI code.
"""

from pathlib import Path
import yaml

# resolving the config directory relative to this file
CONFIG_DIR = Path(__file__).parent
DEFAULT_CONFIG_PATH = CONFIG_DIR / 'default.yaml'
USER_CONFIG_PATH = CONFIG_DIR / 'user.yaml'


def _deep_merge_dicts(base: dict, override: dict) -> dict:
    """
    Recursively merges two dictionaries.
    - Values from `override` take precedence
    - Nested dictionaries are merged, not replaced

    Returns the resulting merged dictionary.
    """
    
    # starting from the base
    result = base.copy()
    
    for key, value in override.items():
        # merging recursively if both values are dictionaries
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge_dicts(result[key], value)
        
        # otherwise, overriding the base value completely
        else:
            result[key] = value
    
    return result


def load_config() -> dict:
    """
    Loads the configuration settings from the YAML files in this folder, merging the
    default and user settings in the process.
    
    Returns the merged dictionary.
    """
    
    # loading the default config (which must exist)
    with open(DEFAULT_CONFIG_PATH, 'r', encoding = 'utf-8') as f:
        default_config: dict = yaml.safe_load(f)
    
    # if present, loading the user config
    # (it should be present, but that issue can be handled when relevant;
    #  we don't need it to exist to resolve this functionality)
    if USER_CONFIG_PATH.exists():
        with open(USER_CONFIG_PATH, 'r', encoding = 'utf-8') as f:
            user_config: dict = yaml.safe_load(f) or dict()
    # if not present, we just initialize it to an empty dictionary
    else:
        user_config = dict()
    
    # returning the merged product of the two config dictionaries
    return _deep_merge_dicts(default_config, user_config)


# loading the config settings once so the rest of the app can just import CONFIG
CONFIG = load_config()