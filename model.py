from sqlalchemy import Integer, String, Column
from database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String, nullable=False)
    subject =Column(String, nullable=False)
    body =Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    draft = Column(String, default="")