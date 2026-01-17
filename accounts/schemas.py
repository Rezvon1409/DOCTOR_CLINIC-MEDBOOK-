from pydantic import BaseModel, model_validator, field_validator, EmailStr, ValidationError,ConfigDict
from .models import Permission

class RegisterShcema(BaseModel):
    username:str
    password:str
    confirm_password:str
    bio:str = None
    department:str = None
    
    model_config = ConfigDict(extra="forbid")
    
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


class AddUserShcema(BaseModel):
    username:str
    password:str
    confirm_password:str
    is_staff:bool = False
    is_superuser:bool = False
    
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
    permissions:list["PermissionSchema"]
    roles:list["RoleSchema"]
    
    model_config=ConfigDict(from_attributes=True)
    
    
class SetUserPermissionsSchema(BaseModel):
    user_id:int
    permissions:list[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("Fields are required")
        return value

class SetRolePermissionsSchema(BaseModel):
    role_id:int
    permissions:list[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("Fields are required")
        return value


class PermissionSchema(BaseModel):
    id:int
    name:str
    description:str


class RoleSchema(BaseModel):
    id:int
    name:str
    permissions:list[PermissionSchema]
    
class AddRoleSchema(BaseModel):
    name:str
    
    @field_validator("name", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("role name must be set!")
        return value


class SetRoleToUserSchema(BaseModel):
    user_id:int
    roles:list[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(value):
        if not value:
            raise ValueError("Fields are required!")
        return value


