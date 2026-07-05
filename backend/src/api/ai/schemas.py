from pydantic import BaseModel, Field

class EmailMessageSchema(BaseModel):
    subject: str 
    content: str 
    invalid_request: bool | None = Field(default=None, description="Indicates if the request is invalid")   

class SupervisorMessageSchema(BaseModel):
    content : str