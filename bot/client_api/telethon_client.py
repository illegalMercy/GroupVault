from telethon import TelegramClient
from telethon.sessions import StringSession


class TelethonClient:
    def __init__(self, session_string):
        self.client = self.get_client(session_string=session_string)

    async def __aenter__(self):
        try:
            await self.client.connect()
        except Exception as e:
            raise ConnectionError()
        
        if not await self.client.is_user_authorized():
            raise ConnectionError()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

    @staticmethod
    def get_client(api_id=1, api_hash='1', session_string=None):
        try:
            client = TelegramClient(
                StringSession(session_string),
                api_id=api_id, api_hash=api_hash,
                device_model="iPhone 13 Pro Max",
                system_version="14.8.1",
                app_version="8.4",
                lang_code="en",
                system_lang_code="en-US",
                connection_retries=2, timeout=5
            )
        except Exception as e:
            raise ValueError("Failed to get a teleton client: {}".format(session_string))
        return client


