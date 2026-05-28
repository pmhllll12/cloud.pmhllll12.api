from titanic.adapter.inbound.api.V1.james_router import james_router
from titanic.adapter.inbound.api.V1.titanic_query_router import router as titanic_query_router
from titanic.adapter.inbound.api.V1.walter_router import walter_router

__all__ = [
    "james_router",
    "titanic_query_router",
    "walter_router",
]
