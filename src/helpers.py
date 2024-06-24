import re
from functools import reduce
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
    text = message.text.lower()
    words = text.split()

    base_cost = 1
    char_cost = len(text) * 0.05
    word_cost = sum(0.1 if len(w) <= 3 else 0.2 if len(w) <= 7 else 0.3 for w in words)
    third_vowel_cost = sum(0.3 for i, char in enumerate(text) if char.lower() in "aeiou" and (i + 1) % 3 == 0)
    length_penalty = 5 if len(text) > 100 else 0
    unique_word_bonus = -2 if len(set(words)) == len(words) else 0
    costs = [base_cost, char_cost, word_cost, third_vowel_cost, length_penalty, unique_word_bonus]
    subtotal = reduce(lambda x, y: x + y, costs)

    is_palindrome = re.sub(r"[^a-z]", "", text) == re.sub(r"[^a-z]", "", text)[::-1]
    palindrome_multiplier = 2 if is_palindrome else 1

    return max(1, subtotal) * palindrome_multiplier
