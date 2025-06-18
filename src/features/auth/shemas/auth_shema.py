from pydantic import BaseModel, field_validator, EmailStr


class RegisterSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('The password must be at least 8 characters')
        return password


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('The password must be at least 8 characters')
        return password
