import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from psycopg import OperationalError
from psycopg_pool import PoolClosed, PoolTimeout

from app.database import my_pool
from app.routers import (
    balances,
    expense_payers,
    expense_splits,
    expenses,
    group_members,
    groups,
    settle_ups,
    users,
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    my_pool.open()
    yield
    # Shutdown
    my_pool.close()


app = FastAPI(title="Fair-Share-API",
              description="Backend API for Fair Share expense tracking application",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc",
              lifespan=lifespan
              )


@app.exception_handler(PoolTimeout)
@app.exception_handler(PoolClosed)
@app.exception_handler(OperationalError)
async def database_unavailable_handler(request: Request, exc: Exception):
    logger.warning(
        "Database unavailable for %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return JSONResponse(
        status_code=503,
        content={"detail": "Database is temporarily unavailable. Please try again later."},
        headers={"Retry-After(s)": "10"},
    )


# Routers
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(balances.router)
app.include_router(group_members.router)
app.include_router(expenses.router)
app.include_router(expense_splits.router)
app.include_router(expense_payers.router)
app.include_router(settle_ups.router)


@app.get("/")
def root():
    return {"Message": "Fair Share API is Running"}