from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from ..handlers import Routers
from ..admin.handlers import AdminRouters


def create_dispatcher():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(*Routers.get_routers(), *AdminRouters.get_routers())
    
    return dp