from pydantic import BaseModel, model_validator, field_validator, EmailStr, ValidationError,ConfigDict

class RegisterShcema(BaseModel):
    username:str
    password:str
    confirm_password:str
    
    @field_validator("*", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("Fields are required")
        return value

    @model_validator(mode="before")
    def check_passwords_match(value):
        if value["password"] != value["confirm_password"]:
            raise ValueError("Passwords do not match")
        return value


class LoginShcema(BaseModel):
    username:str
    password:str
    
    @field_validator("*", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("Fields are required")
        return value
    
class UserSchema(BaseModel):
    id:int
    username:str
    department:str
    
    model_config=ConfigDict(from_attributes=True)