from datetime import datetime, timezone

from models.enums import EventCategory
from pydantic import BaseModel, Field, field_validator


class EventSchema(BaseModel):
    title: str = Field(min_length = 5, max_length = 100)
    description: str = Field(min_length = 5, max_length = 20000)
    date_time : datetime
    capacity: int
    category: EventCategory

        
    @field_validator('capacity')
    @classmethod
    def check_capacity(cls, value):
        if value < 0:
            raise ValueError("Event capacity must be a valid number. It can't be lower than 0")
        return value
        
    @field_validator('date_time')
    @classmethod
    def check_date_time(cls, value):
        now = datetime.now(timezone.utc)

        if value.tzinfo is None:
            value = value.replace(tzinfo = timezone.utc)

        if value <= now:
            raise ValueError("The event start time must be in the future.")
        return value
