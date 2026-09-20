from fastapi import FastAPI

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

app = FastAPI(title="Fair-Share-API",
              description="Backend API for Fair Share expense tracking application",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc")


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