"""Unit tests for ConfigManager."""

import json
import pytest
from pathlib import Path
from configvault import ConfigManager


class TestConfigManagerInitialization:
    """Test ConfigManager initialization and validation."""

    def test_init_with_valid_json_file(self, tmp_path):
        """Test initialization with a valid JSON file."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value"}')
        cm = ConfigManager(str(config_file))
        assert cm.path == config_file

    def test_init_with_valid_yaml_file(self, tmp_path):
        """Test initialization with a valid YAML file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("key: value")
        cm = ConfigManager(str(config_file))
        assert cm.path == config_file

    def test_init_with_valid_yml_file(self, tmp_path):
        """Test initialization with a valid YML file."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("key: value")
        cm = ConfigManager(str(config_file))
        assert cm.path == config_file

    def test_init_with_valid_toml_file(self, tmp_path):
        """Test initialization with a valid TOML file."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("key = \"value\"")
        cm = ConfigManager(str(config_file))
        assert cm.path == config_file

    def test_init_with_missing_file(self):
        """Test initialization with a non-existent file."""
        with pytest.raises(FileNotFoundError):
            ConfigManager("/nonexistent/config.json")

    def test_init_with_unsupported_format(self, tmp_path):
        """Test initialization with an unsupported file format."""
        config_file = tmp_path / "config.xml"
        config_file.write_text("<config></config>")
        with pytest.raises(ValueError, match="Unsupported format"):
            ConfigManager(str(config_file))


class TestConfigManagerLoading:
    """Test configuration file loading."""

    def test_load_json(self, tmp_path):
        """Test loading a JSON configuration file."""
        config_file = tmp_path / "config.json"
        config_data = {"database": {"host": "localhost", "port": 5432}}
        config_file.write_text(json.dumps(config_data))
        cm = ConfigManager(str(config_file))
        assert cm.load() == config_data

    def test_load_json_caching(self, tmp_path):
        """Test that load() caches data and doesn't re-read file."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value"}')
        cm = ConfigManager(str(config_file))
        first_load = cm.load()
        config_file.write_text('{"key": "modified"}')
        second_load = cm.load()
        assert first_load == second_load
        assert first_load["key"] == "value"

    def test_load_yaml(self, tmp_path):
        """Test loading a YAML configuration file."""
        pytest.importorskip("yaml")
        config_file = tmp_path / "config.yaml"
        config_file.write_text("database:\n  host: localhost\n  port: 5432")
        cm = ConfigManager(str(config_file))
        data = cm.load()
        assert data["database"]["host"] == "localhost"
        assert data["database"]["port"] == 5432

    def test_load_yaml_empty_file(self, tmp_path):
        """Test loading an empty YAML file returns empty dict."""
        pytest.importorskip("yaml")
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")
        cm = ConfigManager(str(config_file))
        assert cm.load() == {}

    def test_load_toml(self, tmp_path):
        """Test loading a TOML configuration file."""
        config_file = tmp_path / "config.toml"
        config_file.write_text('[database]\nhost = "localhost"\nport = 5432')
        cm = ConfigManager(str(config_file))
        data = cm.load()
        assert data["database"]["host"] == "localhost"
        assert data["database"]["port"] == 5432

    def test_load_invalid_json(self, tmp_path):
        """Test loading an invalid JSON file raises ValueError."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{invalid json}")
        cm = ConfigManager(str(config_file))
        with pytest.raises(ValueError, match="Failed to parse config file"):
            cm.load()


class TestConfigManagerGetKey:
    """Test dot-notation key retrieval."""

    def test_get_top_level_key(self, tmp_path):
        """Test retrieving a top-level key."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"name": "myapp"}')
        cm = ConfigManager(str(config_file))
        assert cm.get("name") == "myapp"

    def test_get_nested_key(self, tmp_path):
        """Test retrieving a nested key with dot notation."""
        config_file = tmp_path / "config.json"
        config_data = {"database": {"host": "localhost", "port": 5432}}
        config_file.write_text(json.dumps(config_data))
        cm = ConfigManager(str(config_file))
        assert cm.get("database.host") == "localhost"
        assert cm.get("database.port") == 5432

    def test_get_deeply_nested_key(self, tmp_path):
        """Test retrieving a deeply nested key."""
        config_file = tmp_path / "config.json"
        config_data = {"app": {"db": {"primary": {"host": "db.example.com"}}}}
        config_file.write_text(json.dumps(config_data))
        cm = ConfigManager(str(config_file))
        assert cm.get("app.db.primary.host") == "db.example.com"

    def test_get_missing_key_returns_default(self, tmp_path):
        """Test that missing keys return the default value."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value"}')
        cm = ConfigManager(str(config_file))
        assert cm.get("missing.key") is None
        assert cm.get("missing.key", "default") == "default"

    def test_get_key_with_default_value(self, tmp_path):
        """Test retrieving a key with a custom default."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"app": {"timeout": 30}}')
        cm = ConfigManager(str(config_file))
        assert cm.get("app.timeout") == 30
        assert cm.get("app.retries", 3) == 3

    def test_get_traverses_nested_none(self, tmp_path):
        """Test that traversing through None returns default."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"app": {"config": null}}')
        cm = ConfigManager(str(config_file))
        assert cm.get("app.config.timeout", "default") == "default"

    def test_get_non_dict_traversal_returns_default(self, tmp_path):
        """Test that traversing non-dict values returns default."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"app": "value"}')
        cm = ConfigManager(str(config_file))
        assert cm.get("app.nested", "default") == "default"
