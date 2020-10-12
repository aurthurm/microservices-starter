from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from graphql.execution.executors.asyncio import AsyncioExecutor

from app.database.session import database # noqa

from app.api.api_v1.api import api_router # noqa
from app.core.config import settings # noqa

from starlette.graphql import GraphQLApp
from app.gql.schema import gql_schema # noqa

app = FastAPI(
    title=settings.PROJECT_NAME, 
    docs_url="/users/docs",
    redoc_url="/users/redoc",
    openapi_url=f"/users{settings.API_V1_STR}/openapi.json"
)

# These dont work well with uvicorn

# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
    
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=f"/users{settings.API_V1_STR}")
app.add_route("/users/graphql", GraphQLApp(schema=gql_schema, executor_class=AsyncioExecutor))
