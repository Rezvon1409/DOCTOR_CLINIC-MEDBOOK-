from pydantic import BaseModel, model_validator, field_validator, EmailStr, ValidationError, ConfigDict
from .models import Permission
from datetime import date, datetime
from typing import Optional, List


class RegisterSchema(BaseModel):  # ✅ Ислоҳ: "Schema" ба ҷои "Shcema"
    username: str
    password: str
    confirm_password: str
    bio: str = None
    department: str = None
    
    model_config = ConfigDict(extra="forbid")
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required")
        return value

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values


class AddUserSchema(BaseModel):  # ✅ Ислоҳ: "Schema" ба ҷои "Shcema"
    username: str
    password: str
    confirm_password: str
    is_staff: bool = False
    is_superuser: bool = False
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required")
        return value

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values


class LoginSchema(BaseModel):  # ✅ Ислоҳ: "Schema" ба ҷои "Shcema"
    username: str
    password: str
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required")
        return value
    
    
class UserSchema(BaseModel):
    id: int
    username: str
    department: str
    permissions: List["PermissionSchema"]
    roles: List["RoleSchema"]
    
    model_config = ConfigDict(from_attributes=True)
    
    
class SetUserPermissionsSchema(BaseModel):
    user_id: int
    permissions: List[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required")
        return value


class SetRolePermissionsSchema(BaseModel):
    role_id: int
    permissions: List[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required")
        return value


class PermissionSchema(BaseModel):
    id: int
    name: str
    description: str


class RoleSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema]
    
    
class AddRoleSchema(BaseModel):
    name: str
    
    @field_validator("name", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Role name must be set!")
        return value


class SetRoleToUserSchema(BaseModel):
    user_id: int
    roles: List[int]
    
    @field_validator("*", mode="before")
    def not_empty_validators(cls, value):
        if not value:
            raise ValueError("Fields are required!")
        return value


# ==================== MEDICAL SYSTEM SCHEMAS ====================

class PatientCreateSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    gender: str
    passport_number: str
    phone: str
    address: str
    region: str
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    emergency_contact: str
    emergency_phone: str


class PatientSchema(PatientCreateSchema):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DoctorCreateSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    specialization: str
    license_number: str
    qualification: str
    experience_years: int
    phone: str
    email: str
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    consultation_fee: Optional[float] = None



class DoctorSchema(DoctorCreateSchema):
    id: int
    user_id: Optional[int] = None   # ✅ ислоҳ
    is_available: bool
    hospital_name: Optional[str] = None
    department_name: Optional[str] = None
    age: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)



from datetime import date, time

class AppointmentCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    hospital_id: int
    appointment_date: date
    appointment_time: time   # ✅ на str
    status: Optional[str] = "scheduled"
    symptoms: Optional[str] = None
    notes: Optional[str] = None


class AppointmentSchema(AppointmentCreateSchema):
    id: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    patient_name: Optional[str] = None  # ✅ Илова кардан
    doctor_name: Optional[str] = None  # ✅ Илова кардан
    hospital_name: Optional[str] = None  # ✅ Илова кардан
    
    model_config = ConfigDict(from_attributes=True)


# ==================== HOSPITAL SYSTEM SCHEMAS ====================

class HospitalCreateSchema(BaseModel):
    name: str
    region: str
    city: str
    address: str
    phone: str
    email: Optional[str] = None
    hospital_type: str = "public"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class HospitalSchema(HospitalCreateSchema):
    id: int
    is_active: bool
    created_at: datetime
    doctor_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class DepartmentCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    hospital_id: int


class DepartmentSchema(DepartmentCreateSchema):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DoctorScheduleCreateSchema(BaseModel):
    doctor_id: int
    day_of_week: int  # 0-6
    start_time: str  # "09:00"
    end_time: str    # "17:00"
    slot_duration: int = 30


class DoctorScheduleSchema(DoctorScheduleCreateSchema):
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


# Forward references for recursive schemas
PermissionSchema.model_rebuild()
RoleSchema.model_rebuild()


class PrescriptionCreateSchema(BaseModel):
    medical_record_id: int  
    medicine_name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None


class PrescriptionSchema(PrescriptionCreateSchema):
    id: int
    prescribed_date: date
    model_config = ConfigDict(from_attributes=True)


class MedicalRecordCreateSchema(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    symptoms: str
    examination_notes: Optional[str] = None
    recommendations: Optional[str] = None
    next_visit_date: Optional[date] = None

class MedicalRecordSchema(MedicalRecordCreateSchema):
    id: int
    created_at: datetime
    prescriptions: List[PrescriptionSchema] = []
    model_config = ConfigDict(from_attributes=True)
