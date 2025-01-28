# Twitter Bot

A Twitter bot built with Python that leverages OpenAI and LangChain technologies.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv twitter
   source twitter/bin/activate  # On Unix/macOS
   # or
   twitter\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes all necessary dependencies:
   - openai
   - langchain
   - tweepy (Twitter API)
   - python-dotenv (for environment variables)
   - And other supporting libraries

## Configuration

Add the following environment variables:
OPENAI_API_KEY=your_openai_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
CDP_API_KEY_NAME=your_cdp_api_key_name
CDP_API_KEY_PRIVATE_KEY=$'your_cdp_api_key_private_key'


## Development

This project uses VS Code as the recommended IDE. The workspace settings are configured in `.vscode/settings.json` for optimal Python development experience.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

