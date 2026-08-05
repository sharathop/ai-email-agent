import time

from database import SessionLocal
from model import Email

from llm import generate_reply


print("Worker Started...")


while True:

    db = SessionLocal()

    email = (
        db.query(Email)
        .filter(Email.status == "Pending")
        .first()
    )

    if email:

        print(f"Processing Email {email.id}")

        reply = generate_reply(email)

        email.draft = reply

        email.status = "Completed"

        db.commit()

        print("Completed")

    db.close()

    time.sleep(2)