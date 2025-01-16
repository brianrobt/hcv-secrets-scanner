# hcv-secrets-scanner

This is a very incomplete CLI utility that checks the integrity of your Hashicorp Vault secrets.
The project's purpose is to be used as a learning tool for me to understand how to build a Python CLI with Typer.

This project was adapted from the [rp-todo
project](https://github.com/realpython/materials/tree/master/typer-cli-python/source_code_step_7).
I used Grok and Cursor to assist me with writing the code for the sake of reducing the amount of
time I spent on this project.

## Installation

```bash
git clone https://github.com/brianrobt/hcv-secrets-scanner.git
cd hcv-secrets-scanner
poetry install
source .venv/bin/activate
```

## Getting Started

First, you'll need to create a [Hashicorp Cloud
account](https://portal.cloud.hashicorp.com/sign-up?product_intent=vault). Next, set up a new app
in Vault Secrets. Once you've done that, you'll need to create a new Service Principal key for the
app. You also need your project ID, which can be found in the URL of your project in the HCP UI
(e.g., `HCP_PROJECT_ID=e9147846-dd0e-4c5e-b5a7-574719a160be` if your project's URL is `https://portal.cloud.hashicorp.com/services/secrets/apps/sample-app/secrets?project_id=e9147846-dd0e-4c5e-b5a7-574719a160be`).

With your Service Principal key, ID, and project ID set the following environment variables:

```bash
export HCP_CLIENT_ID=<your-client-id>
export HCP_CLIENT_SECRET=<your-client-secret>
export HCP_PROJECT_ID=<your-project-id>
```

`hcvss` generates a new API token every time you run a command. Find more information on how to
use `hcvss` below.

## Usage

### Check secrets integrity remotely

```bash
python -m hcvss check
```

### Fetch secrets from HCP

```bash
python -m hcvss fetch

```
