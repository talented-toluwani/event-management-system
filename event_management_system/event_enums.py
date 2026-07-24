from enum import Enum


class UserRole(Enum):
    '''A list of constant strings that will be used in the user role. This is to prevent unnecessary 
    strings that will be used in the program'''
    PARTICIPANT = "participant"
    ADMIN = "admin"

class EventCategory(Enum):
    '''A list of constant strings that will be used in the event category. This is to prevent 
    unnecessary strings that will be used in the program'''
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    SPORTS = "sports"
    OTHER = "other"

class EventStatus(Enum):
    '''A list of constant strings that will be used in the event status. This is to prevent 
    unnecessary strings in the program'''
    WORKSHOP = "workshop"
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"