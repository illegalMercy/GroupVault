import hashlib
import logging
from typing import Coroutine, Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from config import config


class YoomoneyWebhook:
    def __init__(self, success_callback: Coroutine[Any, Any, None], 
                 host: str = '127.0.0.1', port: int = 8000, endpoint: str = "/payment"):
        self.host = host
        self.port = port
        self.endpoint = f"/{endpoint}" if endpoint[0] != "/" else endpoint
        self.success_callback = success_callback
        self.app = FastAPI()

    async def start(self):
        if not self.app:
            return
        
        self.register_endpoint(self.endpoint)
        logging.info(f"Webhook is listening at http://{self.host}:{self.port}{self.endpoint}")

        runner = uvicorn.Server(
            config=uvicorn.Config(
                self.app, 
                host=self.host, 
                port=self.port, 
                access_log=False, 
                log_level="error")
            )
        await runner.serve()

    def register_endpoint(self, endpoint: str):
        self.app.post(endpoint)(self.handle_webhook)

    async def handle_webhook(self, request: Request):
        try:
            x_forwarded_for = request.headers.get("X-Forwarded-For")
            client_ip = x_forwarded_for or request.client.host
            logging.info(f'Incoming webhook from {client_ip}')

            request_data = await self.parse_request(request)
            await self.success_callback(request_data)
            
            return 200
        except Exception as e:
            logging.error(f"Error handling webhook: {e}")
            return 500
        
    async def parse_request(self, request: Request):
        form_data = await request.form()
        request_data = dict(form_data)

        if not self.verify_signature(request_data, config.yoomoney_secret_key.get_secret_value()):
            logging.error(f"Invalid request signature")
            raise HTTPException(status_code=400, detail="Invalid request signature")
        
        return request_data
    
    def verify_signature(self, request_data: dict, secret_key: str):
        param_keys = [
            'notification_type',
            'operation_id',
            'amount',
            'currency',
            'datetime',
            'sender',
            'codepro',
            'secret_key',
            'label'
        ]
        params = [
            secret_key if key == 'secret_key' else request_data.get(key)
            for key in param_keys
        ]
        params_string = "&".join(params)
        sha1_hash = hashlib.sha1(params_string.encode('utf-8')).hexdigest()
    
        return sha1_hash == request_data.get('sha1_hash')

