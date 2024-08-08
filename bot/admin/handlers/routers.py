from .menu import router as menu_router
from .accounts import router as accounts_router
from .groups import router as groups_router
from .price import router as price_router


class AdminRouters:
    
    routers = [
        menu_router,
        accounts_router,
        groups_router,
        price_router
    ]

    @classmethod
    def get_routers(cls):
        return cls.routers
    