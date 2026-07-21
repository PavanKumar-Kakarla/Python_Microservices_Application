from pydantic import BaseModel, EmailStr, ConfigDict


class UserProfileCreate(BaseModel):

    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None = None



class UserProfileUpdate(BaseModel):

    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserProfileResponse(BaseModel):

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )