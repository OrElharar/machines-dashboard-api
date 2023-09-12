from pydantic.dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    password: str
    full_name: str
    updated_at: datetime
    created_at: datetime
