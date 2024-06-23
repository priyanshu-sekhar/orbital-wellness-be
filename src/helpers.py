from typing import Type, TypeVar

import httpx
from pydantic import BaseModel

from src.models import Message

T = TypeVar("T", bound=BaseModel)


async def fetch_data(url, model: Type[T]) -> T:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return model.parse_obj(response.json())


def calculate_credits_cost(message: Message) -> float:
    # TODO: Implement this function
    # TODO use pydantic models for message
    message_text = message.text
    return 1.0