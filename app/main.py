from fastapi import FastAPI

from app.routers import groups, users, group_members, expenses, expense_splits, expense_payers, settle_ups

app = FastAPI()

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(group_members.router)
app.include_router(expenses.router)
app.include_router(expense_splits.router)
app.include_router(expense_payers.router)
app.include_router(settle_ups.router)




@app.get("/")
def root():
    return {"Message": "Fair Share API Is Running"}


