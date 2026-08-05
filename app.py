from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from database import Base
from database import engine
from queue_service import redis_client
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

# Push email ID into Redis queue
    redis_client.lpush("email_queue", email.id)
    print(f"Queued Email ID: {email.id}")
    print("Queue Length:", redis_client.llen("email_queue"))

    return {
         "message": "Email queued successfully",
         "email_id": email.id,
         "status": email.status
}

@app.get("/emails")
def get_emails(db: Session = Depends(get_db)):

    emails = db.query(Email).all()

    return emails