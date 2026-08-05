import logging
from datetime import datetime

logger = logging.getLogger(__name__)

import uuid

import utils.exceptions
from models.enums import EventCategory, EventStatus
from models.models import Event
from pydantic import ValidationError
from utils.validators import EventSchema


class EventService:
    def __init__(self, event_repository, registration_repository):
        self.event_repository = event_repository
        self.registration_repository = registration_repository

    def create_event(
        self,
        title: str,
        description: str,
        date_time: datetime,
        capacity: int,
        category: EventCategory,
    ) -> Event:
        """Creates a new event that users can register for.

        Args:
            title(str): The name of the event.
            description(str): A detailed description of the event.
            date_time(datetime): The date and time when the event will occur.
            capacity(int): The maximum number of participants allowed.
            category(enum): The category of the event.

        Returns:
            Event: The newly created event object with a unique ID and UPCOMING status.

        Raises:
            ValidationError: If the input data does not match the event schema.
            Exception: For any other errors during event creation.
        """

       
        try:
            validated_data = EventSchema(
                title=title,
                description=description,
                date_time=date_time,
                capacity=capacity,
                category= category            )  # validates the input data with the event schema

            event_id = str(uuid.uuid4())  # generates unique event ids
            current_participants = 0

            event = Event(
                event_id=event_id,
                title=validated_data.title,
                description=validated_data.description,
                date_time=validated_data.date_time,
                max_capacity=validated_data.capacity,
                category=validated_data.category,
                current_participants=current_participants,
                status=EventStatus.UPCOMING,
            )  # creates an event object using the validated data

            saved_event = self.event_repository.create(event)
            return saved_event

        except ValidationError:
            logger.error(" The input data did not match the event schema")
            raise

        except Exception:
            logger.error(
                "Error occurred while trying to implement the event service class"
            )
            raise

    def get_event(self, event_id: int) -> Event:
        """Retrieves a specific event by its ID.

        Args:
            event_id(int): The unique identifier for the event.

        Returns:
            Event: The event object corresponding to the given ID.

        Raises:
            EventNotFound: If no event with the given ID exists.
        """
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            logger.error(f"Event with event id {event_id} was not found")
            raise utils.exceptions.EventNotFound(event_id)

        return event

    def get_all_events(self):
        events = self.event_repository.get_all_events()
        return events

    def get_upcoming_events(self):
        upcoming_events = self.event_repository.get_upcoming()
        return upcoming_events

    def get_events_by_user(self, user_id):
        return self.event_repository.get_events_by_user(user_id)

    def search_events(self, keyword: str):
        """Searches for events matching a specific keyword.

        Args:
            keyword(str): The search term to find in event titles or descriptions.

        Returns:
            list: A list of events matching the keyword, or an empty list if none found.

        Raises:
            ValueError: If keyword is None or contains only whitespace.
        """
        if keyword is None:
            logger.error("The user did not enter in a valid keyword")
            raise ValueError(f"Keyword {keyword} must be a valid text!")

        elif not keyword.strip():
            logger.error("Keyword is empty or has just whitespace")
            raise ValueError("The search keyword cannot be empty!")

        matching_events = self.event_repository.search(keyword)

        return matching_events or []

    def filter_by_category(self, category: str):
        """Filters events by a specific category.

        Args:
            category(str): The category to filter events by.

        Returns:
            list: A list of events in the specified category, or an empty list if none found.

        Raises:
            ValueError: If category is None or contains only whitespace.
        """
        if category is None:
            logger.error("The user did not enter in a valid category")
            raise ValueError(f"The category {category} must be a valid text")

        category = category.strip()
        if not category:
            logger.error("Category is empty or has only white spaces")
            raise ValueError("Category cannot be empty!")

        filtered_events = self.event_repository.get_by_category(category)
        return filtered_events or []

    def update_event(self, event):
        return self.event_repository.update(event)

    def register_user(self, user_id: int, event_id: int):
        """Registers a user for an event.

        Args:
        user_id(int):The unique identifier for the user.
        event_id(int): The unique identifier for the event.

        Returns:
        Registration: The newly created registration object.

        Raises:
        ValueError: If user_id or event_id are invalid.
        EventNotFound: If the event does not exist.
        DuplicateRegistration: If the user is already registered for the event.
        EventFullError: If the event has reached full capacity.
        """

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer")

        # fetches the event
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise utils.exceptions.EventNotFound(event_id)

        if self.registration_repository.is_registered(user_id, event_id):
            raise utils.exceptions.DuplicateRegistration(user_id, event_id)

        if event.is_full:
            raise utils.exceptions.EventFullError(user_id, event_id)

        registration = self.registration_repository.register(user_id, event_id)
        return registration

    def unregister_user(self, user_id: int, event_id: int):

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer!")

        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer.")

        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise utils.exceptions.EventNotFound(event_id)

        is_registered = self.registration_repository.is_registered(user_id, event_id)

        if is_registered is False:
            raise utils.exceptions.NotRegistered(user_id, event_id)

        removed_registration = self.registration_repository.unregister(
            user_id, event_id
        )

        return removed_registration

    def cancel_event(self, event_id: int):

        if not isinstance(event_id, int) or (event_id <= 0):
            raise ValueError("Event ID must be a positive integer.")

        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise utils.exceptions.EventNotFound(event_id)

        if event.status == EventStatus.CANCELLED:
            raise utils.exceptions.EventAlreadyCancelled(event_id)

        event.status = EventStatus.CANCELLED
        event_status_update = self.event_repository.update(event)
        return event_status_update

    def delete_event(self, event_id: int):

        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer.")

        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise utils.exceptions.EventNotFound(event_id)

        self.event_repository.delete(event_id)
        return True
