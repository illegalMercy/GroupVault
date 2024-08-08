import logging
import asyncio

from config import config
from database import create_db, init_db
from bot.handlers.group_sale import successful_payment
from yoomoney.payment_webhook import YoomoneyWebhook
from bot.utils.loggers import setup_logger, change_libs_log_lvl
from bot.factory import create_bot, create_dispatcher, set_commands


async def main():
    setup_logger(level=logging.INFO)
    change_libs_log_lvl()

    await create_db()
    await init_db()

    bot = create_bot(config.bot_token.get_secret_value())
    dp = create_dispatcher()
    wh = YoomoneyWebhook(lambda request_data: successful_payment(bot, request_data))

    asyncio.create_task(wh.start())

    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        pass
