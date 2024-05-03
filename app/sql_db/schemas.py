from pydantic import BaseModel, EmailStr, Field


class PromptBase(BaseModel):
    prompt: str
    response: str


class PromptCreate(PromptBase):
    pass


class Prompt(PromptBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr = Field()
    username: str
    role: str = "user"


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: str
    prompts: list[Prompt] = []

    class Config:
        orm_mode = True
