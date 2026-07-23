# configvault

A minimal, extensible configuration manager supporting YAML, TOML, and JSON formats.

## Installation

```bash
git clone https://github.com/yourusername/configvault.git
cd configvault
pip install -e .
```

## Quick Start

```python
from configvault import ConfigManager

cm = ConfigManager('config.yaml')
db_host = cm.get('database.host')
```

## Supported Formats

- YAML (.yaml, .yml)
- TOML (.toml)
- JSON (.json)

## License

MIT
