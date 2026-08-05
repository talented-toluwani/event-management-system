from dataclasses import dataclass
from datetime import datetime, timezone

from models.enums import EventCategory, EventStatus, UserRole


@dataclass
class Event:
    event_id:str 
    title: str 
    description: str 
    date_time: datetime 
    max_capacity: int 
    category:EventCategory
    current_participants: int 
    status: EventStatus

    @property
    def is_full(self) -> bool: #checks if the number of participant is more than the maxium capacity required, and returns the complementary boolean answer
            return self.current_participants >= self.max_capacity
    
    @property
    def available_spots(self) -> int: #checks the number of available spots left
        return self.max_capacity - self.current_participants
    
    @property
    def is_upcoming(self):
        return self.date_time > datetime.now(timezone.utc)
    
@dataclass
class User:
    user_id: str = "user_id"
    name: str = "name"
    email: str = "email"
    role: str = "role"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
