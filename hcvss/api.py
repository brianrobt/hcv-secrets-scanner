"""
This module provides the API for HCVSS.
"""

import os
import requests
from .constants import HCP_API_BASE_URL


def configure_kv_engine(secret_mount_path, max_versions=0, cas_required=False, delete_version_after="0s"):
    """
    Configure the KV engine for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/config"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
    data = {
        "max_versions": max_versions,
        "cas_required": cas_required,
        "delete_version_after": delete_version_after
    }
    response = requests.post(url, headers=headers, json=data)


def read_kv_engine_config(secret_mount_path):
    """
    Read the KV engine configuration for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/config"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def read_secret_version(secret_mount_path, path, version=0):
    """
    Read the secret version for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/data/{path}?version={version}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def create_secret(secret_mount_path, path, data):
    """
    Create a secret for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/data/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
    response = requests.post(url, headers=headers, json=data)


def update_secret(secret_mount_path, path, data):
    """
    Update a secret for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/data/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def patch_secret(secret_mount_path, path, data):
    """
    Patch a secret for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/data/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
    response = requests.patch(url, headers=headers, json=data)


def read_secret_subkeys(secret_mount_path, path, version=0, depth=0):
    """
    Read the subkeys for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/subkeys/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def delete_secret(secret_mount_path, path):
    """
    Delete a secret for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/data/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def delete_secret_versions(secret_mount_path, path, versions):
    """
    Delete the secret versions for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/delete/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def undelete_secret_versions(secret_mount_path, path, versions):
    """
    Undelete the secret versions for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/undelete/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def destroy_secret_versions(secret_mount_path, path, versions):
    """
    Destroy the secret versions for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/destroy/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def list_secrets(secret_mount_path, path):
    """
    List the secrets for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/metadata/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
    response = requests.get(url, headers=headers)
    return response.json()


def read_secret_metadata(secret_mount_path, path):
    """
    Read the secret metadata for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/metadata/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
    response = requests.get(url, headers=headers)
    return response.json()


def update_secret_metadata(secret_mount_path, path, max_versions=0, cas_required=False, delete_version_after="0s", custom_metadata=None):
    """
    Update the secret metadata for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/metadata/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def patch_secret_metadata(secret_mount_path, path, max_versions=0, cas_required=False, delete_version_after="0s", custom_metadata=None):
    """
    Patch the secret metadata for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/metadata/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }


def delete_secret_metadata_and_all_versions(secret_mount_path, path):
    """
    Delete the secret metadata and all versions for the HCVSS project.
    """
    url = f"{HCP_API_BASE_URL}{secret_mount_path}/metadata/{path}"
    headers = {
        "X-Vault-Token": os.environ.get("VAULT_TOKEN")
    }
