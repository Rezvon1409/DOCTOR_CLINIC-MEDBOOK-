from sqlalchemy import Integer, String, DateTime, Table, Column, ForeignKey, false, Time, Date, Float, Text , Boolean
from datetime import datetime, date, time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from server.models import BaseModel


user_permissions = Table(
    "user_permissions",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)

role_permissions = Table(
    "role_permissions",
    BaseModel.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)

user_roles = Table(
    "user_roles",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(nullable=True)
    department: Mapped[str] = mapped_column(String, default="sales")
    is_staff: Mapped[bool] = mapped_column(server_default=false(), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(server_default=false(), nullable=False)
    
    roles: Mapped[list["Role"]] = relationship("Role", secondary=user_roles, back_populates="users")
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary=user_permissions, back_populates="users")


class Permission(BaseModel):
    __tablename__ = "permissions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    users: Mapped[list["User"]] = relationship("User", secondary=user_permissions, back_populates="permissions")
    roles: Mapped[list["Role"]] = relationship("Role", secondary=role_permissions, back_populates="permissions")


class Role(BaseModel):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship("User", secondary=user_roles, back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary=role_permissions, back_populates="roles")


class BlackListTokens(BaseModel):
    __tablename__ = "blacklisted_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)




class Hospital(BaseModel):
    __tablename__ = "hospitals"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    region: Mapped[str] = mapped_column(String(50))  
    city: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(300))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    hospital_type: Mapped[str] = mapped_column(String(20), default="public")  
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    doctors: Mapped[list["Doctor"]] = relationship(back_populates="hospital", cascade="all, delete-orphan")
    departments: Mapped[list["Department"]] = relationship(back_populates="hospital", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="hospital", cascade="all, delete-orphan")


class Department(BaseModel):
    __tablename__ = "departments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    hospital: Mapped["Hospital"] = relationship(back_populates="departments")
    doctors: Mapped[list["Doctor"]] = relationship(back_populates="department", cascade="all, delete-orphan")


class Patient(BaseModel):
    __tablename__ = "patients"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(10))  
    passport_number: Mapped[str] = mapped_column(String(20), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(String(300))
    region: Mapped[str] = mapped_column(String(50))
    blood_type: Mapped[str] = mapped_column(String(3), nullable=True)
    allergies: Mapped[str] = mapped_column(Text, nullable=True)
    chronic_diseases: Mapped[str] = mapped_column(Text, nullable=True)
    emergency_contact: Mapped[str] = mapped_column(String(100))
    emergency_phone: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    user: Mapped["User"] = relationship("User")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    medical_records: Mapped[list["MedicalRecord"]] = relationship(back_populates="patient", cascade="all, delete-orphan")



class Doctor(BaseModel):
    __tablename__ = "doctors"
    
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)
    specialization: Mapped[str] = mapped_column(String(100))
    license_number: Mapped[str] = mapped_column(String(50), unique=True)
    qualification: Mapped[str] = mapped_column(String(100))  
    experience_years: Mapped[int] = mapped_column(Integer)
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"), nullable=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=True)
    
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    consultation_fee: Mapped[float] = mapped_column(Float, nullable=True)
    
   
    user: Mapped["User"] = relationship("User")
    hospital: Mapped["Hospital"] = relationship(back_populates="doctors")
    department: Mapped["Department"] = relationship(back_populates="doctors")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor", cascade="all, delete-orphan")
    working_hours: Mapped[list["DoctorSchedule"]] = relationship(back_populates="doctor", cascade="all, delete-orphan")
    medical_records: Mapped[list["MedicalRecord"]] = relationship(back_populates="doctor", cascade="all, delete-orphan")

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )



class DoctorSchedule(BaseModel):
    __tablename__ = "doctor_schedules"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    day_of_week: Mapped[int] = mapped_column(Integer) 
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    slot_duration: Mapped[int] = mapped_column(Integer, default=30)  
    is_active: Mapped[bool] = mapped_column(default=True)
    
    doctor: Mapped["Doctor"] = relationship(back_populates="working_hours")


class Appointment(BaseModel):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"))
    
    appointment_date: Mapped[date] = mapped_column(Date)
    appointment_time: Mapped[time] = mapped_column(Time)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")  
    symptoms: Mapped[str] = mapped_column(Text, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
   
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    hospital: Mapped["Hospital"] = relationship(back_populates="appointments")
    medical_record: Mapped["MedicalRecord"] = relationship(back_populates="appointment", uselist=False)


class MedicalRecord(BaseModel):
    __tablename__ = "medical_records"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    
    diagnosis: Mapped[str] = mapped_column(Text)
    symptoms: Mapped[str] = mapped_column(Text)
    examination_notes: Mapped[str] = mapped_column(Text, nullable=True)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)
    next_visit_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    appointment: Mapped["Appointment"] = relationship(back_populates="medical_record")
    patient: Mapped["Patient"] = relationship(back_populates="medical_records")
    doctor: Mapped["Doctor"] = relationship(back_populates="medical_records")
    prescriptions: Mapped[list["Prescription"]] = relationship(back_populates="medical_record", cascade="all, delete-orphan")


class Prescription(BaseModel):
    __tablename__ = "prescriptions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    medical_record_id: Mapped[int] = mapped_column(ForeignKey("medical_records.id"))
    medicine_name: Mapped[str] = mapped_column(String(200))
    dosage: Mapped[str] = mapped_column(String(100))  
    frequency: Mapped[str] = mapped_column(String(100))  
    duration: Mapped[str] = mapped_column(String(100)) 
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    prescribed_date: Mapped[date] = mapped_column(Date, default=date.today)
    
    
    medical_record: Mapped["MedicalRecord"] = relationship(back_populates="prescriptions")
              