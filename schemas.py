from pydantic import BaseModel

class EmailRequest(BaseModel):

    customer: str
    subject: str
    body: str


class EmailResponse(BaseModel):
    id: int
    customer: str
    subject: str
    body: str
    status: str
    draft: str

    class Config:
        from_orm = True

