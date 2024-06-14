from pydantic import BaseModel, Field


class EventMessage(BaseModel):
    msg_id: str = Field(...)
    msg_type: str = Field(...)
    msg_data: dict = Field(...)
