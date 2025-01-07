# ffxiv-encounter-compiler-v2

A Discord bot that fetches and summarizes FFLogs reports for the "Future's Rewritten (Ultimate)" raid in Final Fantasy XIV.

## Description

This bot listens for FFLogs report URLs in Discord messages and responds with a summary of the report, including total pulls, raid duration, and wipes by phases. This project is heavily inspired by and a rewrite of [FFXIV-Encounter-Compiler](https://github.com/AleXwern/FFXIV-Encounter-Compiler) to work with the FFLogs v2 API and Future's Rewritten (Ultimate) since it's not maintained anymore.

Currently, this is a minimum viable product for personal usage for my static and not thoroughly tested. Use at your own risk.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/cld-r/ffxiv-encounter-compiler-v2.git
    cd ffxiv-encounter-compiler-v2
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Create a `config.conf` file**:
    ```ini
    BOT_TOKEN=your_discord_bot_token
    CLIENT_ID=your_fflogs_client_id
    CLIENT_SECRET=your_fflogs_client_secret
    ```

## Usage

1. **Run the bot**:
    ```sh
    python main.py
    ```

2. **Interact with the bot**:
    - Send a message in Discord with an FFLogs report URL (e.g., `https://www.fflogs.com/reports/your_report_id`).
    - The bot will respond with a summary of the report.

## Configuration

- **config.conf**: Contains the bot token and FFLogs API credentials.
    ```ini
    BOT_TOKEN=your_discord_bot_token
    CLIENT_ID=your_fflogs_client_id
    CLIENT_SECRET=your_fflogs_client_secret
    ```

## TODO
- [ ] Add support for other ultimates besides "Future's Rewritten (Ultimate)".
- [ ] Improve error handling and logging.
- [ ] Add unit tests for the main functionalities.
- [ ] Add support for writing data directly to Google Sheets.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.