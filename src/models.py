from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    timestamp: str
    report_id: Optional[int] = None
    text: str


class Report(BaseModel):
    name: str
    credit_cost: float


class Usage(BaseModel):
    message_id: int
    timestamp: str
    report_name: Optional[str] = None
    credits_used: float


class FetchMessagesResponse(BaseModel):
    messages: list[Message]


class GetUsageResponse(BaseModel):
    usage: list[Usage]
