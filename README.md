# Jira-Google Calendar Sync API

## Overview

This Python-based API enables two-way synchronization between Jira Cloud issues and Google Calendar events.

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Jira Cloud account
- API credentials for both platforms

## Setup

1. Create virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

Create a `.env` file with the following:

    ```bash
    JIRA_USERNAME=your_jira_username
    JIRA_API_TOKEN=your_jira_api_token
    JIRA_SERVER_URL=https://your-domain.atlassian.net
    GOOGLE_CREDENTIALS_PATH=path/to/google_credentials.json
    ```

## Authentication

- For Jira: Use API token from Atlassian Account
- For Google: Use OAuth 2.0 credentials from Google Cloud Console

## Deployment

Deploy on Google Cloud Run or App Engine with the provided `app.yaml` configuration.

## Features

- Sync Jira issues to Google Calendar
- Sync Google Calendar events to Jira
- Configurable sync intervals
- Error handling and logging

## Documentation

Detailed documentation can be found in the `docs` directory.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## 📜 License

<a href="http://www.wtfpl.net/"><img
       src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png"
       width="88" height="31" alt="WTFPL" /></a>

This repository is licensed under the [DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE](http://www.wtfpl.net/)

  ![license image](choose-freedom.png)

## Support

For support, please open an issue in the repository.

## Acknowledgments
