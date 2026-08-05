from sqlalchemy import Column, Integer, String, Text
from database import Base

class Email(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    customer = Column(String)

    subject = Column(String)

    body = Column(Text)

    draft = Column(Text)

    status = Column(String)

    category = Column(String, default="Unknown")   # NEW