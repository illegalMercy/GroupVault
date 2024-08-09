<div align="center">
  <a href="https://github.com/illegalMercy/GroupVault">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GroupVault</h3>

  <p align="center">
    Телеграм бот для продажи групп с отлёжкой
  </p>
  <a href="https://github.com/illegalMercy/GroupVault/blob/main/README.ru.md">
    <img src="https://img.shields.io/badge/язык-ru-green.svg" alt='ru'></img>
  </a>
  <a href="https://github.com/illegalMercy/GroupVault/blob/main/README.md">
    <img src="https://img.shields.io/badge/lang-en-blue.svg" alt='en'></img>
  </a>
</div>

## Содержание
- [Описание](#-описание)
  - [Возможности](#возможности) 
- [Технологии](#%EF%B8%8F-технологии)
- [Установка](#-установка)
  - [Настройка проекта](#настройка-проекта)
  - [Запуск как сервис Systemd](#запуск-как-сервис-systemd)
- [Настройка оплаты](#-настройка-оплаты)
  - [Настройка Nginx](#настройка-nginx)
  - [Настройка HTTP-уведомлений YooMoney](#настройка-http-уведомлений-yoomoney) 
- [Контакты](#%EF%B8%8F-контакты)
- [Лицензия](#-лицензия)

## 💡 Описание

Python телеграм-бот, который позволяет продавать телеграм-группы с определённым сроком отлёжки. Бот выполняет роль магазина, где пользователи могут выбирать и приобретать группы. Оплата осуществляется через сервис [YooMoney](https://yoomoney.ru).

###  Возможности

**Бот**:
  - Отправка пригласительной ссылки, после оплаты.
  - Передача права владения группой.
  - Определение возраста групп.

**Пользователь**:
  - Выбор и покупка групп с необходимым сроком отлёжки.
  - Оплата с помощью платежей YooMoney.
  
**Администратор**:
  - Загрузка телеграм аккаунтов для последующего выбора групп, которыми они владеют.
  - Выбор папки аккаунта, из которой будут загружены группы и выставлены на продажу.
  - Изменение и добавление цены для определенного срока отлёжки группы.

## 🛠️ Технологии

**Язык**: Python 3.12

**Библиотеки**:
- [aiogram](https://pypi.org/project/aiogram/) - для работы с Telegram Bot API.
- [telethon](https://pypi.org/project/Telethon/) - для взаимодействия с Telegram Client API.
- [sqlalchemy](https://pypi.org/project/SQLAlchemy/) - для работы с базой данных через ORM.
- [aiosqlite](https://pypi.org/project/aiosqlite/) - для асинхронной работы с SQLite.
- [fastapi](https://pypi.org/project/fastapi/) - для создания веб-хука оплаты через YooMoney.

## 🚀 Установка 

### Настройка проекта 

1. Клонируйте репозиторий:
```bash
git clone https://github.com/illegalMercy/GroupVault.git
```

2. Перейдите в директорию проекта:
```bash
cd GroupVault
```

3. Создайте и активируйте виртуальное окружение:
```bash
# Создание
python -m venv venv

# Активация
source venv/bin/activate
```

4. Установите необходимые зависимости:
```bash
pip install -r requirements.txt
```

5. Настройте переменные окружения. Используйте `env_sample` в качестве шаблона:
- `BOT_TOKEN`: [Токен вашего телеграм-бота](https://t.me/BotFather).
- `YOOMONEY_SECRET_KEY`: [Секретный ключ для платежей YooMoney](https://yoomoney.ru/transfer/myservices/http-notification).
- `YOOMONEY_WALLET_ID:` Номер кошелька YooMoney.
- `SQLITE_DATABASE_PATH`: Путь к файлу базы данных SQLite.
- `ADMIN_ID`: Телеграм ID пользователя-администратора бота.

6. Запустите бота:
```bash
python main.py
```

### Запуск как сервис Systemd

1. Создайте файл сервиса systemd. Например, `group_vault.service`:
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
- `Description`: Описание сервиса. В данном случае, это “Group Vault Bot”, что помогает идентифицировать сервис.
- `WorkingDirectory`: Рабочая директория, в которой будет выполняться сервис.
- `Environment`:  В данном случае, это путь к виртуальному окружению проекта.
- `ExecStart`: - Команда, которая будет выполнена для запуска сервиса.

2.  Перезагрузите systemd, чтобы применить изменения:
```bash
sudo systemctl daemon-reload
```

3. Запустите сервис и добавьте его в автозагрузку:
```bash
sudo systemctl start group_vault.service
sudo systemctl enable group_vault.service
```

## 💳 Настройка оплаты

### Настройка Nginx

1. Для начала установите **Nginx**, если он еще не установлен:
```bash
sudo apt update
sudo apt install nginx
```

2. Создайте новый файл конфигурации. Например, `group_vault_payment`:
```bash
sudo vim /etc/nginx/sites-available/group_vault_payment
```

```nginx
server {
    listen 80;
    server_name ваш_домен_или_IP; 

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

> **Примечание**:
> По умолчанию веб-хук для получения уведомлений о платежах использует порт `8000`

3. Создайте символическую ссылку на файл конфигурации в каталоге `sites-enabled`:
```bash
sudo ln -s /etc/nginx/sites-available/group_vault_payment /etc/nginx/sites-enabled
```

4. Проверьте конфигурацию на наличие ошибок и перезапустите Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Настройка HTTP-уведомлений YooMoney

1. Перейдите на [страницу настройки HTTP-уведомлений](https://yoomoney.ru/transfer/myservices/http-notification) YooMoney.

2. Вставьте ваш IP-адрес в поле `Куда отправлять (URL сайта)` и добавьте `/payment`. Например: `http://123.123.123.123/payment`

>**Примечание**:
>По умолчанию веб-хук для получения уведомлений о платежах использует эндпоинт `/payment`

3. Получите секрет для проверки подлинности HTTP-уведомлений, нажав `Показать секрет`. Его требуется указать в переменных окружения.

4. Включите опцию `Отправлять HTTP-уведомления` и нажмите `Готово`.

[Подробнее о том, как работают HTTP-уведомления](https://yoomoney.ru/docs/wallet/using-api/notification-p2p-incoming)

## 🗨️ Контакты

- **Email**:  [al.ostaenkov@gmail.com](al.ostaenkov@gmail.com)
- **Telegram**:  [@illegalMercy](https://t.me/illegalMercy)

## 📃 Лицензия

Этот проект лицензирован на условиях лицензии MIT. Подробности см. в файле [LICENSE](link).
