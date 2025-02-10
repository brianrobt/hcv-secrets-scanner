import pytest
from unittest.mock import patch, Mock
from hcvss.api import HCVSSClient

@pytest.fixture
def client():
    """Create a test client with a dummy token"""
    return HCVSSClient(vault_token="test-token")

@pytest.fixture
def mock_response():
    """Create a mock response object"""
    mock = Mock()
    mock.json.return_value = {"data": {"foo": "bar"}}
    return mock

def test_init_with_token():
    """Test client initialization with explicit token"""
    client = HCVSSClient(vault_token="test-token")
    assert client.vault_token == "test-token"
    assert client.headers == {"X-Vault-Token": "test-token"}

@patch.dict('os.environ', {'VAULT_TOKEN': 'env-token'})
def test_init_with_env_token():
    """Test client initialization with environment token"""
    client = HCVSSClient()
    assert client.vault_token == "env-token"
    assert client.headers == {"X-Vault-Token": "env-token"}

class TestSecretOperations:
    """Group tests for secret operations"""

    @patch('requests.post')
    def test_create_secret(self, mock_post, client, mock_response):
        """Test creating a secret"""
        mock_post.return_value = mock_response

        result = client.create_secret(
            secret_mount_path="secret",
            path="my-secret",
            cas=0,
            data={"password": "secret123"}
        )

        mock_post.assert_called_once_with(
            f"{client.secrets_scanner.base_url}/secret/data/my-secret",
            headers=client.headers,
            json={"password": "secret123"}
        )
        assert result == {"data": {"foo": "bar"}}

    @patch('requests.get')
    def test_read_secret_version(self, mock_get, client, mock_response):
        """Test reading a secret version"""
        mock_get.return_value = mock_response

        result = client.read_secret_version(
            secret_mount_path="secret",
            path="my-secret",
            version=1
        )

        mock_get.assert_called_once_with(
            f"{client.secrets_scanner.base_url}/secret/data/my-secret?version=1",
            headers=client.headers
        )
        assert result == {"data": {"foo": "bar"}}

    @patch('requests.delete')
    def test_delete_secret(self, mock_delete, client, mock_response):
        """Test deleting a secret"""
        mock_delete.return_value = mock_response

        result = client.delete_secret(
            secret_mount_path="secret",
            path="my-secret"
        )

        mock_delete.assert_called_once_with(
            f"{client.secrets_scanner.base_url}/secret/data/my-secret",
            headers=client.headers
        )
        assert result == {"data": {"foo": "bar"}}

class TestMetadataOperations:
    """Group tests for metadata operations"""

    @patch('requests.get')
    def test_read_secret_metadata(self, mock_get, client, mock_response):
        """Test reading secret metadata"""
        mock_get.return_value = mock_response

        result = client.read_secret_metadata(
            secret_mount_path="secret",
            path="my-secret"
        )

        mock_get.assert_called_once_with(
            f"{client.secrets_scanner.base_url}/secret/metadata/my-secret",
            headers=client.headers
        )
        assert result == {"data": {"foo": "bar"}}

    @patch('requests.post')
    def test_update_secret_metadata(self, mock_post, client, mock_response):
        """Test updating secret metadata"""
        mock_post.return_value = mock_response

        result = client.update_secret_metadata(
            secret_mount_path="secret",
            path="my-secret",
            max_versions=5,
            cas_required=True,
            custom_metadata={"owner": "team-a"}
        )

        mock_post.assert_called_once()
        assert result == {"data": {"foo": "bar"}}