from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app.models.student import Student
from app.schemas.student import StudentCreate

app = FastAPI(title="FERJEE Student System")

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to FERJEE Student System API"}

@app.post("/students", response_model=StudentCreate)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Verificar se RG ou CPF já existem
    if db.query(Student).filter(Student.rg == student.rg).first():
        raise HTTPException(status_code=400, detail="RG já cadastrado")
    if db.query(Student).filter(Student.cpf == student.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    # Criar novo aluno
    db_student = Student(
        name=student.name,
        rg=student.rg,
        cpf=student.cpf,
        address=student.address,
        phone=student.phone
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return student