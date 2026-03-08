import pytest
import os
import yaml
import sys

# Ensure scripts directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_config_exists():
    assert os.path.exists("config.yaml"), "config.yaml is missing"

def test_config_parsing():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert "random_seed" in config
    assert "indexing" in config
    assert "preprocessing" in config
    
def test_import_scripts():
    import scripts.config
    assert scripts.config.config is not None
    assert scripts.config.config["random_seed"] == 42
