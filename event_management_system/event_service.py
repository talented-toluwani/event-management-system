import logging
import uuid
from typing import List

import event_exceptions
from event_enums import EventStatus
from event_models import Event
from event_schema import EventSchema
from pydantic import ValidationError


class EventService:
    def __init__(self,event_repository, registration_repository):
       self.event_repository = event_repository
       self.registration_repository = registration_repository

    def create_event(self, title, description, date_time, capacity, category):
        try:

            validated_data = EventSchema(
            title = title,
            description = description,
            date_time = date_time,
            capacity = capacity,
            category = category
            ) # validates the input data with the event schema 
       
            event_id = str(uuid.uuid4()) # generates uniqye event ids 
            current_participants = 0
            status = EventStatus.UPCOMING

            event = Event(
            event_id = event_id,
            title = validated_data.title,
            description = validated_data.description,
            date_time = validated_data.date_time,
            max_capacity = validated_data.capacity,
            category = validated_data.category,
            current_participants = current_participants,
            status = status
    )# creates an event objecr using the validated data
            
            saved_event = self.event_repository.create(event)
            return saved_event
        
        except ValidationError:
            logging.error(" The input data did not match the event schema", exc_info= True)
            raise 

        except Exception:
            logging.error("An error occured while trying to implement the event service class", exc_info=True)
            raise

    
    def get_event(self, event_id: int) -> Event: 
           event = self.event_repository.get_by_id(event_id)

           if event is None:
               logging.error(f"Event with event id {event_id} was  not found")
               raise event_exceptions.EventNotFound(event_id)

           return event
        

    def get_all_events(self) -> List[Event]:
        events = self.event_repository.get_all_events()
        return events


    def get_upcoming_events(self) -> List[Event]:
        upcoming_events = self.event_repository.get_upcoming()
        return upcoming_events
   
    def get_events_by_user(self, user_id):
        return self.event_repository.get_events_by_user(user_id)
    

    def search_events(self, keyword:str ) -> List[Event]:
        if keyword is None:
            logging.error("The user did not enter in a valid keyword", exc_info = True)
            raise ValueError(f"Keyword {keyword} must be a valid text!")
        
        elif not keyword.strip():
           logging.error("Keywords is empty or has just whitespace", exc_info=True)
           raise ValueError("The search keyword cannot be empty!")
        
        matching_events = self.event_repository.search(keyword)

        return matching_events or []
            

    def filter_by_category(self, category:str) -> List[Event]:

        if category is None:
            logging.error("The user did not enter in a valid category", exc_info = True)
            raise ValueError(f"The category {category} must be a valid text")

        category = category.strip()
        if not category:
            logging.error("Category is empty or has only white spaces")
            raise ValueError("Category cannot be empty!")
        
        filtered_events = self.event_repository.get_by_category(category)
        return filtered_events or []
    
    def update_event(self, event):
        return self.event_repository.update(event)

    def register_user(self, user_id:int, event_id:int):
        """ Registers a user for an event.

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
        
        #fetches the event
        event = self.event_repository.get_by_id(event_id)  
        
        if event is None:
            raise event_exceptions.EventNotFound(event_id)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        if self.registration_repository.is_registered(user_id, event_id):
            raise event_exceptions.DuplicateRegistration(user_id, event_id)
        
        if event.is_full:
            raise event_exceptions.EventFullError(user_id, event_id)
       
        registration = self.registration_repository.register(user_id, event_id)
        return registration


    def unregister_user(self, user_id:int, event_id:int):

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer!")
         
        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer.")
        
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise event_exceptions.EventNotFound(event_id)
        
        is_registered = self.registration_repository.is_registered(user_id, event_id)
        
        if is_registered is False:
            raise event_exceptions.NotRegistered(user_id, event_id)
        
        removed_registration = self.registration_repository.unregister(user_id, event_id)
        return removed_registration
    
    def cancel_event(self, event_id:int):

        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer.")
        
        event = self.event_repository.get_by_id(event_id)
        
        if event is None:
            raise event_exceptions.EventNotFound(event_id)
        
        if event.status == EventStatus.CANCELLED:
            raise event_exceptions.EventAlreadyCancelled(event_id)
        
        event.status = EventStatus.CANCELLED
        event_status_update = self.event_repository.update(event)
        return event_status_update

    def delete_event(self, event_id:int):

        if not isinstance(event_id, int) or event_id <= 0:
            raise ValueError("Event ID must be a positive integer.")
        
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise event_exceptions.EventNotFound(event_id)
        
        self.event_repository.delete(event_id)
        return True
        
    

       

