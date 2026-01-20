from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from server.settings import get_db
from accounts.views import auth
from accounts.models import *
from accounts.schemas import *
from accounts.permissions import is_authenticated

app = FastAPI(title="Doctor Clinic API")

app.include_router(auth, prefix="/auth", tags=["Auth"])

# ==================== HOSPITAL CRUD ====================

@app.post("/hospitals", response_model=HospitalSchema, dependencies=[Depends(is_authenticated)], tags=["Hospitals"])
async def create_hospital(data: HospitalCreateSchema, db: Session = Depends(get_db)):
    hospital = Hospital(**data.model_dump())
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital

@app.get("/hospitals", response_model=list[HospitalSchema], dependencies=[Depends(is_authenticated)], tags=["Hospitals"])
async def get_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()

@app.get("/hospitals/{hospital_id}", response_model=HospitalSchema, dependencies=[Depends(is_authenticated)], tags=["Hospitals"])
async def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@app.put("/hospitals/{hospital_id}", response_model=HospitalSchema, dependencies=[Depends(is_authenticated)], tags=["Hospitals"])
async def update_hospital(hospital_id: int, data: HospitalCreateSchema, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    for key, value in data.model_dump().items():
        setattr(hospital, key, value)
    db.commit()
    db.refresh(hospital)
    return hospital

@app.delete("/hospitals/{hospital_id}", dependencies=[Depends(is_authenticated)], tags=["Hospitals"])
async def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    db.delete(hospital)
    db.commit()
    return {"detail": "Hospital deleted"}

# ==================== PATIENT CRUD ====================

@app.post("/patients", response_model=PatientSchema, dependencies=[Depends(is_authenticated)], tags=["Patients"])
async def create_patient(data: PatientCreateSchema, db: Session = Depends(get_db)):
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@app.get("/patients", response_model=list[PatientSchema], dependencies=[Depends(is_authenticated)], tags=["Patients"])
async def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.get("/patients/{patient_id}", response_model=PatientSchema, dependencies=[Depends(is_authenticated)], tags=["Patients"])
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=PatientSchema, dependencies=[Depends(is_authenticated)], tags=["Patients"])
async def update_patient(patient_id: int, data: PatientCreateSchema, db: Session = Depends(get_db)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in data.model_dump().items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

@app.delete("/patients/{patient_id}", dependencies=[Depends(is_authenticated)], tags=["Patients"])
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted"}

# ==================== DOCTOR CRUD ====================

@app.post("/doctors", response_model=DoctorSchema, dependencies=[Depends(is_authenticated)], tags=["Doctors"])
async def create_doctor(data: DoctorCreateSchema, db: Session = Depends(get_db)):
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.get("/doctors", response_model=list[DoctorSchema], dependencies=[Depends(is_authenticated)], tags=["Doctors"])
async def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@app.get("/doctors/{doctor_id}", response_model=DoctorSchema, dependencies=[Depends(is_authenticated)], tags=["Doctors"])
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.put("/doctors/{doctor_id}", response_model=DoctorSchema, dependencies=[Depends(is_authenticated)], tags=["Doctors"])
async def update_doctor(doctor_id: int, data: DoctorCreateSchema, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in data.model_dump().items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.delete("/doctors/{doctor_id}", dependencies=[Depends(is_authenticated)], tags=["Doctors"])
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted"}

# ==================== APPOINTMENT CRUD ====================

@app.post("/appointments", response_model=AppointmentSchema, dependencies=[Depends(is_authenticated)], tags=["Appointments"])
async def create_appointment(data: AppointmentCreateSchema, db: Session = Depends(get_db)):
    appointment = Appointment(**data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.get("/appointments", response_model=list[AppointmentSchema], dependencies=[Depends(is_authenticated)], tags=["Appointments"])
async def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@app.get("/appointments/{appointment_id}", response_model=AppointmentSchema, dependencies=[Depends(is_authenticated)], tags=["Appointments"])
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.put("/appointments/{appointment_id}", response_model=AppointmentSchema, dependencies=[Depends(is_authenticated)], tags=["Appointments"])
async def update_appointment(appointment_id: int, data: AppointmentCreateSchema, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in data.model_dump().items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.delete("/appointments/{appointment_id}", dependencies=[Depends(is_authenticated)], tags=["Appointments"])
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted"}


# ==================== MEDICAL RECORD CRUD ====================

@app.post("/medical_records", response_model=MedicalRecordSchema, dependencies=[Depends(is_authenticated)], tags=["Medical Records"])
async def create_medical_record(data: MedicalRecordCreateSchema, db: Session = Depends(get_db)):
    record = MedicalRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/medical_records", response_model=list[MedicalRecordSchema], dependencies=[Depends(is_authenticated)], tags=["Medical Records"])
async def get_medical_records(db: Session = Depends(get_db)):
    return db.query(MedicalRecord).all()

@app.get("/medical_records/{record_id}", response_model=MedicalRecordSchema, dependencies=[Depends(is_authenticated)], tags=["Medical Records"])
async def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@app.put("/medical_records/{record_id}", response_model=MedicalRecordSchema, dependencies=[Depends(is_authenticated)], tags=["Medical Records"])
async def update_medical_record(record_id: int, data: MedicalRecordCreateSchema, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    for key, value in data.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@app.delete("/medical_records/{record_id}", dependencies=[Depends(is_authenticated)], tags=["Medical Records"])
async def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    db.delete(record)
    db.commit()
    return {"detail": "Medical record deleted"}


# ==================== PRESCRIPTION CRUD ====================

@app.post("/prescriptions", response_model=PrescriptionSchema, dependencies=[Depends(is_authenticated)], tags=["Prescriptions"])
async def create_prescription(data: PrescriptionCreateSchema, db: Session = Depends(get_db)):
    prescription = Prescription(**data.model_dump())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription

@app.get("/prescriptions", response_model=list[PrescriptionSchema], dependencies=[Depends(is_authenticated)], tags=["Prescriptions"])
async def get_prescriptions(db: Session = Depends(get_db)):
    return db.query(Prescription).all()

@app.get("/prescriptions/{prescription_id}", response_model=PrescriptionSchema, dependencies=[Depends(is_authenticated)], tags=["Prescriptions"])
async def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).get(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@app.put("/prescriptions/{prescription_id}", response_model=PrescriptionSchema, dependencies=[Depends(is_authenticated)], tags=["Prescriptions"])
async def update_prescription(prescription_id: int, data: PrescriptionCreateSchema, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).get(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for key, value in data.model_dump().items():
        setattr(prescription, key, value)
    db.commit()
    db.refresh(prescription)
    return prescription

@app.delete("/prescriptions/{prescription_id}", dependencies=[Depends(is_authenticated)], tags=["Prescriptions"])
async def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).get(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(prescription)
    db.commit()
    return {"detail": "Prescription deleted"}


# ==================== ROOT ====================

@app.get("/")
async def root():
    return {
        "message": "DOCTOR CLINIC API - National Hospital Management System",
        "version": "1.0.0",
        "system": "Системаи миллӣ барои беморхонаҳои Тоҷикистон",
        "docs": "/docs",
        "redoc": "/redoc"
    }
