# Attendance Tracker Bot

This bot is designed to track attendance through Telegram. It allows users to request attendance reports and sends automated reports periodically.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `schedule` library
- `smtplib` library

## Setup

1. Install the required libraries using pip:

```bash
pip install requests pandas schedule smtplib
```

2. Obtain a Telegram Bot API token from [BotFather](https://core.telegram.org/bots#6-botfather).

3. Replace the `api` variable with your Telegram Bot API token.

4. Configure the email settings by providing your email address and password in the `server.login("", "")` line inside the `send_mail` function.

5. Run the script.

## Usage

1. To trigger attendance tracking, simply message the bot on Telegram.

2. Use the following commands to interact with the bot:

   - `#my_report`: Request your attendance report.
   - `#show_report`: Request to display attendance reports.
   
3. The bot sends automated reports every 1st and 15th of the month.

4. Attendance records are stored in JSON format (`Attendence.json`) and CSV files in the `Attendance_History` directory.

## Important Note

Ensure that the bot has access to read and write files in the directory where the script is running. Also, make sure to configure the bot's permissions appropriately on Telegram.
