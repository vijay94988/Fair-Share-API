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


class ExpenseCreate(BaseModel):
    group_id: int
    description: str
    total_amount: int
    created_by: int