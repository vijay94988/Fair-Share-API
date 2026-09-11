from decimal import Decimal
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class GroupCreate(BaseModel):
    group_name: str
    created_by: int


class GroupMemberCreate(BaseModel):
    group_id: int
    user_id: int


class PayerInput(BaseModel):
    user_id: int
    amount_paid: Decimal

class ExpenseCreate(BaseModel):
    group_id: int
    description: str
    total_amount: Decimal
    created_by: int

    participants: list[int]
    payers: list[PayerInput]


class ExpensePayerCreate(BaseModel):
    expense_id: int
    user_id: int
    amount_paid: Decimal


class ExpenseSplitCreate(BaseModel):
    expense_id: int
    user_id: int
    amount_owed: Decimal


class SettleUpCreate(BaseModel):
    group_id: int
    from_user_id: int
    to_user_id: int
    amount: Decimal

