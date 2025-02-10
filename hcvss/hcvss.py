"""This module provides the Hashivault Secrets Scanner model-controller."""

import json
import os
import subprocess


class SecretsScanner:
    """A class to handle scanning and validation of HashiCorp secrets."""

    def __init__(self):
        """Initialize the SecretsScanner."""
        self.secret_length = 20

        # Check for required environment variables
        required_vars = ['HCP_ORGANIZATION_ID', 'HCP_PROJECT_ID', 'HCP_APP_NAME']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]

        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        self.base_url = (
            "https://api.cloud.hashicorp.com/secrets/2023-11-28"
            f"/organizations/{os.environ['HCP_ORGANIZATION_ID']}"
            f"/projects/{os.environ['HCP_PROJECT_ID']}"
            f"/apps/{os.environ['HCP_APP_NAME']}"
        )

    def check_secrets(self, file_path: str):
        """Check the secrets in the given file."""
        secrets = self._get_secret_values(file_path)

        messages = []

        for secret in secrets:
            if len(secret) <= self.secret_length:
                message = f"Secret {secret} is too short: {len(secret)} characters"
                messages.append(message)
                print(message)

        return messages

    def fetch_hcp_secrets(self) -> dict:
        """
        Fetch secrets from HCP using the provided token.

        Returns:
            dict: A dictionary containing the JSON response from HCP.

        Raises:
            subprocess.CalledProcessError: If the curl or jq command fails.
            json.JSONDecodeError: If the response isn't valid JSON.
        """
        # Construct the curl command
        token = self._generate_hcp_api_token(os.environ.get('HCP_CLIENT_ID'), os.environ.get('HCP_CLIENT_SECRET'))
        url = self.base_url + "/secrets:open"
        cmd = [
            'curl',
            '--location', url,
            '--request', 'GET',
            '--header', f"Authorization: Bearer {token}"
        ]

        try:
            # Execute the curl command and capture its output
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Use jq to format the JSON output (assuming jq is installed)
            jq_cmd = ['jq']
            json_output = subprocess.run(jq_cmd, input=result.stdout, capture_output=True, text=True, check=True).stdout
            # Parse JSON output, printing only enabled for testing purposes
            with open('test_secrets.json', 'w') as f:
                f.write(json_output)
            print(json_output)
            return json.loads(json_output)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            raise

    def _generate_hcp_api_token(self, client_id: str, client_secret: str) -> str:
        """
        Generate an HCP API token using client credentials.

        Args:
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.

        Returns:
            str: The generated HCP API token.

        Raises:
            subprocess.CalledProcessError: If the curl command fails.
            ValueError: If the response doesn't contain an access token.
        """
        cmd = [
            'curl', '--location', 'https://auth.idp.hashicorp.com/oauth2/token',
            '--header', 'Content-Type: application/x-www-form-urlencoded',
            '--data-urlencode', f'client_id={client_id}',
            '--data-urlencode', f'client_secret={client_secret}',
            '--data-urlencode', 'grant_type=client_credentials',
            '--data-urlencode', 'audience=https://api.hashicorp.cloud'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            json_output = result.stdout.strip()
            jq_cmd = ['jq', '-r', '.access_token']
            token_result = subprocess.run(jq_cmd, input=json_output, capture_output=True, text=True, check=True)

            token = token_result.stdout.strip()
            if not token:
                raise ValueError("No access token found in the response.")
            return token
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e.stderr}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def _get_secret_values(self, file_path):
        """
        Get the value from each secret in the JSON data.

        Args:
            file_path: Path to the JSON file containing secrets data.

        Returns:
            list: List of secret values.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
            return []
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} does not contain valid JSON.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

        secrets = data.get('secrets', [])
        return [secret.get('static_version', {}).get('value', 'No value found') for secret in secrets]
