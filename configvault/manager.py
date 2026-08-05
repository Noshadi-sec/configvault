"""Main configuration manager implementation."""

import json
import os
from pathlib import Path


class ConfigManager:
    """Manages configuration files across multiple formats.

    Supports YAML, TOML, and JSON. Auto-detects format by file extension.
    """

    SUPPORTED_FORMATS = {".yaml", ".yml", ".toml", ".json"}

    def __init__(self, config_path: str):
        """Initialize ConfigManager with a configuration file.

        Args:
            config_path: Path to the configuration file.

        Raises:
            ValueError: If file format is not supported.
            FileNotFoundError: If configuration file does not exist.
        """
        self.path = Path(config_path)

        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        ext = self.path.suffix.lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {ext}. Use {self.SUPPORTED_FORMATS}")

        self._data = None

    def load(self) -> dict:
        """Load and parse the configuration file.

        Returns:
            Parsed configuration as dictionary.

        Raises:
            ValueError: If file parsing fails.
        """
        if self._data is not None:
            return self._data

        ext = self.path.suffix.lower()

        try:
            if ext == ".json":
                self._data = self._load_json()
            elif ext in (".yaml", ".yml"):
                self._data = self._load_yaml()
            elif ext == ".toml":
                self._data = self._load_toml()
        except Exception as e:
            raise ValueError(f"Failed to parse config file: {e}")

        return self._data

    def _load_json(self) -> dict:
        """Load JSON configuration file.

        Returns:
            Parsed JSON as dictionary.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_yaml(self) -> dict:
        """Load YAML configuration file.

        Returns:
            Parsed YAML as dictionary.

        Raises:
            ImportError: If PyYAML is not installed.
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "PyYAML is required to load YAML files. "
                "Install it with: pip install pyyaml"
            )

        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}

    def _load_toml(self) -> dict:
        """Load TOML configuration file.

        Returns:
            Parsed TOML as dictionary.

        Raises:
            ImportError: If tomli is not installed (Python < 3.11).
        """
        try:
            if hasattr(__import__("builtins"), "__import__"):
                try:
                    import tomllib
                    with open(self.path, "rb") as f:
                        return tomllib.load(f)
                except ImportError:
                    import tomli
                    with open(self.path, "rb") as f:
                        return tomli.load(f)
        except ImportError:
            raise ImportError(
                "tomli is required to load TOML files on Python < 3.11. "
                "Install it with: pip install tomli"
            )

    def get(self, key: str, default=None):
        """Retrieve configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., 'database.host').
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        data = self.load()
        keys = key.split(".")
        current = data

        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default

        return current
