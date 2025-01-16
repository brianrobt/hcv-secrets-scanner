"""This module provides the Hashivault Secrets Scanner model-controller."""

import json
import os
import subprocess

def check_secrets(file_path: str):
    """Check the secrets in the given file."""
    secrets = get_secret_values(file_path)

    secret_length = 20

    messages = []

    for secret in secrets:
        if len(secret) <= secret_length:
            message = f"Secret {secret} is too short: {len(secret)} characters"
            messages.append(message)
            print(message)

    return messages


def fetch_hcp_secrets() -> dict:
    """
    Fetch secrets from HCP using the provided token.

    Args:
        token (str): The HCP API token for authentication.

    Returns:
        dict: A dictionary containing the JSON response from HCP.

    Raises:
        subprocess.CalledProcessError: If the curl or jq command fails.
        json.JSONDecodeError: If the response isn't valid JSON.
    """
    # Construct the curl command
    token = generate_hcp_api_token(os.environ.get('HCP_CLIENT_ID'), os.environ.get('HCP_CLIENT_SECRET'))
    url = "https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/0cf0027f-5b19-4671-9cfa-bf3a9a84bafb/projects/" + os.environ.get('HCP_PROJECT_ID') + "/apps/sample-app/secrets:open"
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
        # If curl or jq command fails, this exception will be raised
        print(f"Command failed with error: {e.stderr}")
        raise
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        raise


def generate_hcp_api_token(client_id: str, client_secret: str) -> str:
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
    # Construct the curl command
    cmd = [
        'curl', '--location', 'https://auth.idp.hashicorp.com/oauth2/token',
        '--header', 'Content-Type: application/x-www-form-urlencoded',
        '--data-urlencode', f'client_id={client_id}',
        '--data-urlencode', f'client_secret={client_secret}',
        '--data-urlencode', 'grant_type=client_credentials',
        '--data-urlencode', 'audience=https://api.hashicorp.cloud'
    ]

    try:
        # Execute the curl command and capture its output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Parse the JSON output to get the access token
        json_output = result.stdout.strip()
        # Use jq to extract the access_token (assuming jq is installed)
        jq_cmd = ['jq', '-r', '.access_token']
        token_result = subprocess.run(jq_cmd, input=json_output, capture_output=True, text=True, check=True)

        token = token_result.stdout.strip()
        if not token:
            raise ValueError("No access token found in the response.")
        return token
    except subprocess.CalledProcessError as e:
        # If curl or jq command fails, this exception will be raised
        print(f"Command failed with error: {e.stderr}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def get_secret_values(file_path):
    """
    Get the 'value' field from each secret in the JSON data.

    :param json_data: A JSON string or a dictionary containing the secrets data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} does not contain valid JSON.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Extract the list of secrets
    secrets = data.get('secrets', [])

    ret_secrets = []

    # Iterate over each secret and print its value
    for secret in secrets:
        # Access the 'value' under 'static_version'
        value = secret.get('static_version', {}).get('value', 'No value found')
        ret_secrets.append(value)

    return ret_secrets
