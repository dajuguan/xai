# Sentry Linux Client Updater
At present, to operate a Sentry node, users are required to adhere to the [official documentation](https://xai-foundation.gitbook.io/xai-network/xai-blockchain/sentry-node-purchase-and-setup). Nevertheless, given the active development of Sentry, users often face the arduous task of manually updating and restarting their node. This inefficiency poses a significant challenge for node operators.

In response to this issue, I've devised a Python tool while installing the Sentry Linux Client on my server to streamline the server's operational procedures.

This tool offers the following functionalities:

- Automates the download, installation, updating, and initiation of your Sentry node upon each [new release]((https://github.com/xai-foundation/sentry/releases/latest)). It monitors Sentry's latest releases **every 90 seconds**, considering GitHub's api rate limit.
- Sends email notifications when your node experiences downtime or undergoes an update.

Furthermore, to prioritize security, the tool relies on **only one** third-party library, `requests = "2.31.0"`, as part of its dependencies.

# Usage
## Configuration
Create a file named `.env` in the root directory and populate it with your configuration settings, similar to the content found in `.env_copy`. Note that the prv_key refers to your Sentry wallet (operator)'s private key.

> Caution: Safeguard your .env file discreetly and refrain from sharing it with anyone.

## Run Sentry

### Option 1: Using poetry
- [Poetry](https://python-poetry.org/docs/#installation): a tool for dependency management and packaging in Python.
```
curl -sSL https://install.python-poetry.org | python3 -
git clone https://github.com/dajuguan/xai.git
cd xai
poetry install
poetry run python main.py
```
### Option2: Using python
```
git clone https://github.com/dajuguan/xai.git
cd xai
pip install request==2.31.0
python3 main.py
```