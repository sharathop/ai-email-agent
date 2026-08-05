from database import SessionLocal
from model import Email
from queue_service import redis_client

from agent.classifier import classify_email
from agent.router import execute_action

import redis

print("Worker Started...")

while True:

    try:

        print("Waiting for jobs...")

        task = redis_client.brpop(
            "email_queue",
            timeout=5
        )

        print("Task received:", task)

        if task is None:
            continue

        email_id = int(task[1])

        db = SessionLocal()

        email = db.query(Email).filter(
            Email.id == email_id
        ).first()

        if email:

            print(f"\nProcessing Email {email.id}")

            # =====================================
            # Step 1 : Classification
            # =====================================

            classification = classify_email(

                email.subject,

                email.body

            )

            print("\n========== CLASSIFICATION ==========\n")

            print(classification)

            print("\n====================================\n")

            # Save category

            email.category = classification["category"]

            # =====================================
            # Step 2 : Execute Agent
            # =====================================

            reply = execute_action(

                email,

                classification

            )

            # =====================================
            # Step 3 : Save Reply
            # =====================================

            email.draft = reply

            email.status = "Completed"

            db.commit()

            print(f"Completed Email {email.id}")

        db.close()

    except redis.exceptions.TimeoutError:

        continue

    except Exception as e:

        print("\nWorker Error\n")

        print(e)