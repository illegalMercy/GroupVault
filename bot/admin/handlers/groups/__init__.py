from aiogram import Router
from .menu import router as menu_router
from .add_groups import router as add_groups_router
from .del_groups import router as del_groups_router


router = Router()

router.include_routers(
    menu_router, 
    add_groups_router,
    del_groups_router
)