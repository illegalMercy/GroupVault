<div align="center">
  <a href="https://github.com/illegalMercy/GroupVault">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GroupVault</h3>

  <p align="center">
    Telegram bot for selling groups with a resting period
  </p>
  <a href="https://github.com/illegalMercy/GroupVault/blob/main/README.md">
    <img src="https://img.shields.io/badge/lang-en-blue.svg" alt='en'></img>
  </a>
  <a href="https://github.com/illegalMercy/GroupVault/blob/main/README.ru.md">
    <img src="https://img.shields.io/badge/язык-ru-green.svg" alt='ru'></img>
  </a>
</div>

## Table of Contents
- [About](#-about)
  - [Features](#features) 
- [Technologies](#%EF%B8%8F-technologies)
- [Installation](#-installation)
  - [Project Setup](#project-setup)
  - [Running as a Systemd Service](#running-as-a-systemd-service)
- [Payment Setup](#-payment-setup)
  - [Nginx Setup](#nginx-setup)
  - [YooMoney HTTP Notification Setup](#yoomoney-http-notification-setup) 
- [Contacts](#%EF%B8%8F-contacts)
- [License](#-license)

## 💡 About

GroupVault is a Python Telegram bot designed for selling Telegram groups with a resting period. The bot serves as a store where users can browse and purchase groups. Payments are handled through the [YooMoney](https://yoomoney.ru) service.

### Features

**Bot**:
  - Sends an invitation link after payment.
  - Transfers group ownership.
  - Determines the age of groups.

**User**:
  - Selects and buys groups with a desired resting period.
  - Pays via YooMoney.

**Admin**:
  - Uploads Telegram accounts to select and sell the groups they own.
  - Chooses the account folder from which groups will be uploaded and listed for sale.
  - Changes and adds prices for specific resting periods.

## 🛠️ Technologies

**Language**: Python 3.12

**Libraries**:
- [aiogram](https://pypi.org/project/aiogram/) - for working with the Telegram Bot API.
- [telethon](https://pypi.org/project/Telethon/) - for interacting with the Telegram Client API.
- [sqlalchemy](https://pypi.org/project/SQLAlchemy/) - for ORM database interaction.
- [aiosqlite](https://pypi.org/project/aiosqlite/) - for asynchronous SQLite operations.
- [fastapi](https://pypi.org/project/fastapi/) - for creating the YooMoney payment webhook.

## 🚀 Installation 

### Project Setup 

1. Clone the repository:
```bash
git clone https://github.com/illegalMercy/GroupVault.git
```

2. Navigate to the project directory:
```bash
cd GroupVault
```

3. Create and activate a virtual environment:
```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Configure the environment variables. Use `env_sample` as a template:
- `BOT_TOKEN`: [Your Telegram bot token](https://t.me/BotFather).
- `YOOMONEY_SECRET_KEY`: [YooMoney payment secret key](https://yoomoney.ru/transfer/myservices/http-notification).
- `YOOMONEY_WALLET_ID:` YooMoney wallet number.
- `SQLITE_DATABASE_PATH`: Path to the SQLite database file.
- `ADMIN_ID`: Telegram ID of the bot's administrator.

6. Start the bot:
```bash
python main.py
```

### Running as a Systemd Service

1. Create a systemd service file, for example, `group_vault.service`:
```bash
sudo vim /etc/systemd/system/group_vault.service
```

```ini
[Unit]
Description=Group Vault Bot
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/GroupVault
Environment="PATH=/path/to/GroupVault/venv/bin/"
ExecStart=/path/to/GroupVault/venv/bin/python /path/to/GroupVault/main.py
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```
- `Description`: A description of the service. In this case, "Group Vault Bot" to identify the service.
- `WorkingDirectory`: The working directory where the service will run.
- `Environment`: The path to the project's virtual environment.
- `ExecStart`: The command to start the service.

2. Reload systemd to apply the changes:
```bash
sudo systemctl daemon-reload
```

3. Start the service and enable it to run on startup:
```bash
sudo systemctl start group_vault.service
sudo systemctl enable group_vault.service
```

## 💳 Payment Setup

### Nginx Setup

1. First, install **Nginx** if it is not already installed:
```bash
sudo apt update
sudo apt install nginx
```

2. Create a new configuration file, for example, `group_vault_payment`:
```bash
sudo vim /etc/nginx/sites-available/group_vault_payment
```

```nginx
server {
    listen 80;
    server_name your_domain_or_IP; 

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

> **Note**:
> By default, the webhook for receiving payment notifications uses port `8000`.

3. Create a symbolic link to the configuration file in the `sites-enabled` directory:
```bash
sudo ln -s /etc/nginx/sites-available/group_vault_payment /etc/nginx/sites-enabled
```

4. Check the configuration for errors and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### YooMoney HTTP Notification Setup

1. Go to the [YooMoney HTTP Notification settings page](https://yoomoney.ru/transfer/myservices/http-notification).

2. Enter your IP address in the `Where to send (site URL)` field and add `/payment`. For example: `http://123.123.123.123/payment`

>**Note**:
>The default webhook endpoint for receiving payment notifications is `/payment`.

3. Retrieve the secret for authenticating HTTP notifications by clicking `Show secret`. This needs to be specified in the environment variables.

4. Enable the `Send HTTP notifications` option and click `Done`.

[Learn more about how HTTP notifications work](https://yoomoney.ru/docs/wallet/using-api/notification-p2p-incoming)

## 🗨️ Contacts

- **Email**:  [al.ostaenkov@gmail.com](al.ostaenkov@gmail.com)
- **Telegram**:  [@illegalMercy](https://t.me/illegalMercy)

## 📃 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/illegalMercy/GroupVault/blob/main/LICENSE) file for details.
