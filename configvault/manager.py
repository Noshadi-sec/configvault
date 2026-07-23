"""Main configuration manager implementation."""

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
        """
        # TODO: implement format-specific loaders
        pass

    def get(self, key: str, default=None):
        """Retrieve configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., 'database.host').
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        # TODO: implement dot-notation traversal
        pass
