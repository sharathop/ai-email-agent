from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from database import Base
from database import engine
from database import get_db

from model import Email

from schemas import EmailRequest

from llm import generate_reply

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Email Agent"
)


@app.post("/email")
def receive_email(
    request: EmailRequest,
    db: Session = Depends(get_db)
):

    email = Email(

        customer=request.customer,

        subject=request.subject,

        body=request.body,

        status="Pending"

    )

    db.add(email)

    db.commit()

    db.refresh(email)

    return {
    "message": "Email received successfully.",
    "email_id": email.id,
    "status": email.status
}

@app.get("/emails")
def get_emails(db: Session = Depends(get_db)):

    emails = db.query(Email).all()

    return emails