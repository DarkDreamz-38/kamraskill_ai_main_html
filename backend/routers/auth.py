from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Employee


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Prototype demo credentials (SIH presentation build)
DEMO_USER_ID = "nexus123"
DEMO_PASSWORD = "1234"


class LoginRequest(BaseModel):
    email: str  # "Employee ID / Email" field on the login page
    password: str


class LoginResponse(BaseModel):
    token: str
    employee: dict


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    if data.email.strip() != DEMO_USER_ID or data.password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid Employee ID or password"
        )

    employee = db.query(Employee).order_by(Employee.id).first()
    if not employee:
        raise HTTPException(
            status_code=503,
            detail="No employee records found. Run the seed script first."
        )

    return {
        "token": f"demo-token-{employee.id}",
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "role": employee.role,
            "experience": employee.experience,
        },
    }
