from aiogram import Router
from .menu import router as menu_router
from .add_account import router as add_account_router
from .del_account import router as del_account_router


router = Router()

router.include_routers(
    menu_router, 
    add_account_router,
    del_account_router
)