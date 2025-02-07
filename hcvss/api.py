"""
This module provides the API for HCVSS.
"""

import os
import requests
from .constants import HCP_API_BASE_URL
from .hcvss import SecretsScanner


class HCVSSClient:
    """A client for interacting with the HCVSS project."""

    def __init__(self, vault_token=None):
        """
        Initialize the HCVSS client.
        
        Args:
            vault_token (str, optional): The Vault token to use. If not provided,
                                       will attempt to get from VAULT_TOKEN environment variable.
        """
        self.vault_token = vault_token or os.environ.get("VAULT_TOKEN")
        self.headers = {"X-Vault-Token": self.vault_token}
        self.secrets_scanner = SecretsScanner()

    def configure_kv_engine(self, secret_mount_path, max_versions=0, cas_required=False, delete_version_after="0s"):
        """
        Configure the KV engine for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/config"
        data = {
            "max_versions": max_versions,
            "cas_required": cas_required,
            "delete_version_after": delete_version_after
        }
        response = requests.post(url, headers=self.headers, json=data)

    def read_kv_engine_config(self, secret_mount_path):
        """
        Read the KV engine configuration for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/config"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def read_secret_version(self, secret_mount_path, path, version=0):
        """
        Read the secret version for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}?version={version}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_secret(self, secret_mount_path, path, data):
        """
        Create a secret for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def update_secret(self, secret_mount_path, path, data):
        """
        Update a secret for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def patch_secret(self, secret_mount_path, path, data):
        """
        Patch a secret for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def read_secret_subkeys(self, secret_mount_path, path, version=0, depth=0):
        """
        Read the subkeys for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/subkeys/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def delete_secret(self, secret_mount_path, path):
        """
        Delete a secret for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def delete_secret_versions(self, secret_mount_path, path, versions):
        """
        Delete the secret versions for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/delete/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def undelete_secret_versions(self, secret_mount_path, path, versions):
        """
        Undelete the secret versions for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/undelete/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def destroy_secret_versions(self, secret_mount_path, path, versions):
        """
        Destroy the secret versions for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/destroy/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def list_secrets(self, secret_mount_path, path):
        """
        List the secrets for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def read_secret_metadata(self, secret_mount_path, path):
        """
        Read the secret metadata for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def update_secret_metadata(self, secret_mount_path, path, max_versions=0, cas_required=False, delete_version_after="0s", custom_metadata=None):
        """
        Update the secret metadata for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        data = {
            "max_versions": max_versions,
            "cas_required": cas_required,
            "delete_version_after": delete_version_after,
            "custom_metadata": custom_metadata
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def patch_secret_metadata(self, secret_mount_path, path, max_versions=0, cas_required=False, delete_version_after="0s", custom_metadata=None):
        """
        Patch the secret metadata for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        data = {
            "max_versions": max_versions,
            "cas_required": cas_required,
            "delete_version_after": delete_version_after,
            "custom_metadata": custom_metadata
        }
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def delete_secret_metadata_and_all_versions(self, secret_mount_path, path):
        """
        Delete the secret metadata and all versions for the HCVSS project.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.delete(url, headers=self.headers)
        return response.json()
