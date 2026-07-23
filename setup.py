from setuptools import setup, find_packages

setup(
    name="configvault",
    version="0.1.0",
    description="Lightweight configuration manager for YAML, TOML, and JSON",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "black", "flake8"],
    },
)
