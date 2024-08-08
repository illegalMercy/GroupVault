import os
import logging
from logging.handlers import RotatingFileHandler


LOG_DIR = 'logs'
LOG_SIZE = 50000

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def setup_logger(level: int = logging.INFO):
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(level)

    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        format='%(asctime)s %(levelname)s | %(module)s.%(funcName)s | %(message)s',
        datefmt="[%H:%M:%S]",
        level=level,
    )


def log_to_file(name: str, log_file: str, level=logging.INFO, formatter=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = RotatingFileHandler(log_file, maxBytes=LOG_SIZE, backupCount=5, encoding='utf-8')
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s | %(module)s.%(funcName)s | %(message)s',
        datefmt="[%H:%M:%S]"
    ) if not formatter else formatter

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def change_libs_log_lvl():
    error_lvl = ['aiosqlite']
    info_lvl = ['telethon', 'aiogram']

    for logger_lib in error_lvl:
        logging.getLogger(logger_lib).setLevel(logging.ERROR)

    for logger_lib in info_lvl:
        logging.getLogger(logger_lib).setLevel(logging.INFO)
