"""
This module provides the API for HCVSS.
"""

import os
import requests
from .hcvss import SecretsScanner


class HCVSSClient:
    """A client for interacting with the HCVSS project."""

    def __init__(self, vault_token: str = ""):
        """
        Initialize the HCVSS client.

        Args:
            vault_token (str, optional): The Vault token to use. If not provided,
                will attempt to get from VAULT_TOKEN environment variable.
        """
        self.vault_token = vault_token or os.environ.get("VAULT_TOKEN")
        self.headers = {"X-Vault-Token": self.vault_token}
        self.secrets_scanner = SecretsScanner()

    def configure_kv_engine(self, secret_mount_path: str, max_versions: int = 0, cas_required: bool = False, delete_version_after: str = "0s"):
        """
        Configures backend level settings that are applied to every key in the key-value store.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            max_versions (int, optional): The number of versions to keep per key.  This value applies
                to all keys, but a key's metadata can be set to override this value. If set to 0, the
                default, or unset, the backend will  keep 10 versions. Defaults to 0.
            cas_required (bool, optional): If true, all keys will require the cas
                parameter to be set on all write operations. Defaults to False.
            delete_version_after (str, optional): If set, specifies the length of
                time before a version is deleted. Accepts duration format strings like "30s" or "1h".
                Defaults to "0s" (no automatic deletion).
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/config"
        data = {
            "max_versions": max_versions,
            "cas_required": cas_required,
            "delete_version_after": delete_version_after
        }
        response = requests.post(url, headers=self.headers, json=data)

    def read_kv_engine_config(self, secret_mount_path: str):
        """
        Retrieves the current configuration for the secrets backend at the given path.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/config"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def read_secret_version(self, secret_mount_path: str, path: str, version: int = 0):
        """
        Retrieves the secret at the specified location. The metadata fields `created_time`, `deletion_time`,
        `destroyed`, and `version` are version-specific.  The `custom_metadata` field is part of the secret's
        key metadata and is included in the response whether or not the calling token has read access to the
        associated metadata endpoint.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to read.
            version (int, optional): The version of the secret to return.  If not set, the latest version is returned.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}?version={version}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_secret(self, secret_mount_path: str, path: str, options: dict, cas: int, data: dict):
        """
        Creates a new version of a secret at the specified location. If the value does not yet exist, the calling
        token must have an ACL policy granting the create capability. If the value already exists, the
        calling token must have an ACL policy granting the update capability.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to create.
            options (dict): An object that holds options settings.
            cas (int): This flag is required if the backend is configured with cas_required set to true
                on either the secret or the engine's config. If not set, write will be allowed. In order for
                a write to be successful, cas must be set to the current version of the secret.  If set to 0,
                a write will only be allowed if the key doesn't exist as unset keys do not have any version
                information.  Also remember that soft deletes do not remove any underlying version data from
                storage. In order to write to a soft-deleted key, the cas parameter must match the key's current
                version.
            data (dict): The contents of the data dict will be stored and returned on read.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def patch_secret(self, secret_mount_path: str, path: str, options: dict, cas: int, data: dict):
        """
        Provides the ability to patch an existing secret at the specified location. The secret must
        neither be deleted nor destroyed. The calling token must have an ACL policy granting the
        patch capability. Currently, only JSON merge patch is supported and must be specified using
        a Content-Type header value of application/merge-patch+json. A new version will be created
        upon successfully applying a patch with the provided data.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to patch.
            options (dict): An object that holds options settings.
            cas (int): This flag is required if cas_required is set to true on either the secret or
                the engine's config. In order for a write to be successful, cas must be set to the
                current version of the secret. A patch operation must be attempted on an existing
                key, thus the provided cas value must be greater than 0.
            data (dict): The contents of the data map will be applied as a partial update to the
                existing entry via a JSON merge patch to the existing entry.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def read_secret_subkeys(self, secret_mount_path: str, path: str, version: int = 0, depth: int = 0):
        """
        This endpoint provides the subkeys within a secret entry that exists at the requested path.
        The secret entry at this path will be retrieved and stripped of all data by replacing
        underlying values of leaf keys (i.e. non-map keys or map keys with no underlying subkeys) with null.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to read.
            version (int, optional): The version of the secret to return.  If not set, the latest
                version is returned.
            depth (int, optional): Specifies the deepest nesting level to provide in the output. The
                default value 0 will not impose any limit. If non-zero, keys that reside at the
                specified depth value will be artificially treated as leaves and will thus be null
                even if further underlying subkeys exist.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/subkeys/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def delete_secret(self, secret_mount_path: str, path: str):
        """
        This endpoint issues a soft delete of the secret's latest version at the specified location.
        This marks the version as deleted and will stop it from being returned from reads, but the
        underlying data will not be removed. A delete can be undone using the undelete path.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to delete.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/data/{path}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def delete_secret_versions(self, secret_mount_path: str, path: str, versions: list):
        """
        This endpoint issues a soft delete of the specified versions of the secret. This marks the
        versions as deleted and will stop them from being returned from reads, but the underlying
        data will not be removed. A delete can be undone using the undelete path.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to delete.
            versions (list): The versions to be deleted. The versioned data will not be deleted, but
                it will no longer be returned in normal get requests.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/delete/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def undelete_secret_versions(self, secret_mount_path: str, path: str, versions: list):
        """
        Undeletes the data for the provided version and path in the key-value store. This restores
        the data, allowing it to be returned on get requests.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to undelete.
            versions (list): The versions to be undeleted. The versions will be restored and their
                data will be returned on normal get requests.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/undelete/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def destroy_secret_versions(self, secret_mount_path: str, path: str, versions: list):
        """
        Permanently removes the specified version data for the provided key and version numbers from
        the key-value store.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to destroy.
            versions (list): The versions to be destroyed. The versions will be permanently removed
                from the key-value store.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/destroy/{path}"
        response = requests.post(url, headers=self.headers, json={"versions": versions})
        return response.json()

    def list_secrets(self, secret_mount_path: str, path: str):
        """
        This endpoint returns a list of key names at the specified location. Folders are suffixed
        with /. The input must be a folder; list on a file will not return a value. Note that no
        policy-based filtering is performed on keys; do not encode sensitive information in key
        names. The values themselves are not accessible via this command.

        To list secrets for KVv2, a user must have a policy granting them the list capability on
        this /metadata/ path - even if all the rest of their interactions with the KVv2 are via the
        /data/ APIs. Access to at least list the /metadata/ path should typically also be granted.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secrets to list.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def read_secret_metadata(self, secret_mount_path: str, path: str):
        """
        This endpoint retrieves the metadata and versions for the secret at the specified path.
        Metadata is version-agnostic.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to read.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def update_secret_metadata(self, secret_mount_path: str, path: str, max_versions: int = 0, cas_required: bool = False, delete_version_after: str = "0s", custom_metadata: dict = None):
        """
        This endpoint updates the metadata for the secret at the specified path.
        Metadata is version-agnostic.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to update.
            max_versions (int, optional): The number of versions to keep per key.  This value applies
                to all keys, but a key's metadata can be set to override this value.  If set to 0,
                the default, or unset, the backend will keep 10 versions. Defaults to 0.
            cas_required (bool, optional): If true, all keys will require the cas
                parameter to be set on all write operations. Defaults to False.
            delete_version_after (str, optional): Set the delete_version_after value to a duration to
                specify the deletion_time for all new versions written to this key. If not set, the
                backend's delete_version_after will be used. If the value is greater than the
                backend's delete_version_after, the backend's delete_version_after will be used.
                Accepts duration format strings.
            custom_metadata (dict, optional):  A map of arbitrary string to string valued
                user-provided metadata meant to describe the secret.
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

    def patch_secret_metadata(self, secret_mount_path: str, path: str, max_versions: int = 0, cas_required: bool = False, delete_version_after: str = "0s", custom_metadata: dict = None):
        """
        Patches an existing metadata entry of a secret at the specified location. The calling token
        must have an ACL policy granting the patch capability. Currently, only JSON merge patch is
        supported and must be specified using a Content-Type header value of
        application/merge-patch+json. It does not create a new version.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to patch.
            max_versions (int, optional): The number of versions to keep per key. If not set, the
                backend's configured max version is used. Once a key has more than the configured
                allowed versions, the oldest version will be permanently deleted.
            cas_required (bool, optional): If true, all keys will require the cas
                parameter to be set on all write operations.  If false, the backend's configuration will
                be used. Defaults to False.
            delete_version_after (str, optional): Set the delete_version_after value to a duration to
                specify the deletion_time for all new versions written to this key. If not set, the
                backend's delete_version_after will be used. If the value is greater than the
                backend's delete_version_after, the backend's delete_version_after will be used.
                Accepts duration format strings.
            custom_metadata (dict, optional):  A map of arbitrary string to string valued
                user-provided metadata meant to describe the secret.
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

    def delete_secret_metadata_and_all_versions(self, secret_mount_path: str, path: str):
        """
        Permanently deletes the key metadata and all version data for the specified key. All version
        history will be removed.

        Args:
            secret_mount_path (str): The path where the KV secrets engine is mounted.
            path (str): The path to the secret to delete.
        """
        url = f"{self.secrets_scanner.base_url}/{secret_mount_path}/metadata/{path}"
        response = requests.delete(url, headers=self.headers)
        return response.json()
