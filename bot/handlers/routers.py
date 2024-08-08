from .menu import router as menu_router
from .group_sale import router as group_sale_router
from .group_ownership import router as group_ownership_router
from .contacts import router as contacts_router

class Routers:
    
    routers = [
        menu_router,
        group_sale_router,
        group_ownership_router,
        contacts_router
    ]

    @classmethod
    def get_routers(cls):
        return cls.routers
    