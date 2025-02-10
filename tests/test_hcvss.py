import os
import json
import pytest
from unittest.mock import patch, mock_open
from hcvss.hcvss import SecretsScanner

def test_init_with_missing_env_vars():
    """Test initialization fails when environment variables are missing."""
    # Save any existing environment variables
    original_env = {
        'HCP_ORGANIZATION_ID': os.environ.get('HCP_ORGANIZATION_ID'),
        'HCP_PROJECT_ID': os.environ.get('HCP_PROJECT_ID'),
        'HCP_APP_NAME': os.environ.get('HCP_APP_NAME')
    }

    # Clear the environment variables
    for var in original_env:
        if var in os.environ:
            del os.environ[var]

    try:
        with pytest.raises(EnvironmentError) as exc_info:
            SecretsScanner()
        assert "Missing required environment variables" in str(exc_info.value)
    finally:
        # Restore the original environment variables
        for var, value in original_env.items():
            if value is not None:
                os.environ[var] = value

@pytest.fixture
def scanner_with_env_vars():
    """Fixture to provide a SecretsScanner instance with required env vars."""
    env_vars = {
        'HCP_ORGANIZATION_ID': 'test-org',
        'HCP_PROJECT_ID': 'test-project',
        'HCP_APP_NAME': 'test-app',
    }
    with patch.dict(os.environ, env_vars):
        return SecretsScanner()

def test_init_success(scanner_with_env_vars):
    """Test successful initialization with all required environment variables."""
    scanner = scanner_with_env_vars
    assert scanner.secret_length == 20
    assert "test-org" in scanner.base_url
    assert "test-project" in scanner.base_url
    assert "test-app" in scanner.base_url

def test_check_secrets_with_short_secrets(scanner_with_env_vars):
    """Test check_secrets identifies short secrets correctly."""
    mock_json_data = {
        "secrets": [
            {"static_version": {"value": "short"}},
            {"static_version": {"value": "this_is_long_enough_secret"}},
            {"static_version": {"value": "also_short"}},
        ]
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_data))):
        messages = scanner_with_env_vars.check_secrets("fake_path.json")

    assert len(messages) == 2
    assert "Secret short is too short" in messages[0]
    assert "Secret also_short is too short" in messages[1]

def test_get_secret_values_file_not_found(scanner_with_env_vars):
    """Test _get_secret_values handles missing files."""
    result = scanner_with_env_vars._get_secret_values("nonexistent_file.json")
    assert result == []

def test_get_secret_values_invalid_json(scanner_with_env_vars):
    """Test _get_secret_values handles invalid JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = scanner_with_env_vars._get_secret_values("fake_path.json")
    assert result == []

def test_get_secret_values_success(scanner_with_env_vars):
    """Test _get_secret_values successfully extracts secret values."""
    mock_json_data = {
        "secrets": [
            {"static_version": {"value": "secret1"}},
            {"static_version": {"value": "secret2"}},
        ]
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_data))):
        result = scanner_with_env_vars._get_secret_values("fake_path.json")

    assert result == ["secret1", "secret2"]

@patch('subprocess.run')
def test_generate_hcp_api_token_success(mock_run, scanner_with_env_vars):
    """Test successful API token generation."""
    mock_run.side_effect = [
        type('Response', (), {
            'stdout': '{"access_token": "test-token"}',
            'stderr': '',
            'returncode': 0
        }),
        type('Response', (), {
            'stdout': 'test-token\n',
            'stderr': '',
            'returncode': 0
        })
    ]

    token = scanner_with_env_vars._generate_hcp_api_token("test-id", "test-secret")
    assert token == "test-token"

@patch('subprocess.run')
def test_fetch_hcp_secrets_success(mock_run, scanner_with_env_vars):
    """Test successful secrets fetching."""
    mock_run.side_effect = [
        # Mock token generation
        type('Response', (), {
            'stdout': '{"access_token": "test-token"}',
            'stderr': '',
            'returncode': 0
        }),
        type('Response', (), {
            'stdout': 'test-token\n',
            'stderr': '',
            'returncode': 0
        }),
        # Mock secrets fetch
        type('Response', (), {
            'stdout': '{"secrets": []}',
            'stderr': '',
            'returncode': 0
        }),
        type('Response', (), {
            'stdout': '{"secrets": []}',
            'stderr': '',
            'returncode': 0
        })
    ]

    result = scanner_with_env_vars.fetch_hcp_secrets()
    assert isinstance(result, dict)
    assert "secrets" in result