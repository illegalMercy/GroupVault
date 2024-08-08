from aiogram import Router
from .menu import router as menu_router
from .edit_price import router as edit_price_router
from .add_price import router as add_price_router
from .del_price import router as del_price_router


router = Router()

router.include_routers(
    menu_router,
    edit_price_router,
    add_price_router,
    del_price_router
)