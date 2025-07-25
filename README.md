# AutoWagon
_A Discord bot for fetching memes from Reddit and managing a Minecraft server._

## Overview
AutoWagon is a simple yet powerful Discord bot designed to entertain your server with memes directly from Reddit while also providing basic management commands for your Minecraft server. It integrates with the Reddit API to fetch trending memes and includes server automation tools.

## Features
- Fetch random or trending memes from Reddit.
- Minecraft server management commands.
- Lightweight and easy to set up.
- Customizable command prefixes.

## Installation
### Prerequisites
- Python 3.8 or later
- A Discord Bot Token (create one from the [Discord Developer Portal](https://discord.com/developers/applications))
- Reddit API credentials (via [Reddit App Preferences](https://www.reddit.com/prefs/apps))

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/AutoWagon.git
   cd AutoWagon
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your **Discord token** and **Reddit API keys** in a `.env` or config file (details to be added based on project structure).

## Usage
Start the bot with:
```bash
python main.py
```

Once the bot is online, invite it to your Discord server and use commands such as:
```
!meme        # Fetch a random meme
!serverinfo  # Minecraft server info
```

## Project Structure
- `main.py` – Entry point for the bot.
- `keep_alive.py` – Script to keep the bot running (useful for hosting on free services like Replit).
- `requirements.txt` – Python dependencies.
- `setup.py` – Setup file for packaging.

## Contributing
Contributions are welcome!
- Fork the repository
- Create a new branch
- Submit a pull request with your changes

## License
This project is licensed under the MIT License.
