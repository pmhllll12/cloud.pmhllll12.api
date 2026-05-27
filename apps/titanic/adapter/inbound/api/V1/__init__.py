from titanic.adapter.inbound.api.V1.titanic_command_router import router as titanic_command_router
from titanic.adapter.inbound.api.V1.titanic_query_router import router as titanic_query_router

__all__ = [
    "titanic_command_router",
    "titanic_query_router",
]
