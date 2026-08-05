import re

import utils.exceptions
from models.models import User


class UserService:
    def __init__(self, user_repository, registration_repository, event_repository):
        self.user_repository = user_repository
        self.registration_repository = registration_repository
        self.event_repository = event_repository

    
    def register_user(self, name:str, email:str, role:str):

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")
        
        if len(name) < 2 or len(name) > 50:
            raise ValueError("The length of the name must be between 2 and 50 characters.")
      
        email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    
        if not re.fullmatch(email_regex, email.strip().lower()):
            raise ValueError(f"'{email}' is not a valid email format.")


        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError(f"A user with the email {email} already exists.")

        print("Creating User")
        new_user = None

        try:
            new_user = User(
            user_id = None,
            name = name.strip(),
            email = email.strip().lower(),
            role = role.value
            )

        except Exception as e:
            print(f"Unable to create user {e}")
            return None

        print("Created user")

        created_user = self.user_repository.create(new_user)
        return created_user
        
    
    def login(self, email:str):

        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            return existing_user
        
        return None
    

    def get_user(self, user_id:int):

        existing_user = self.user_repository.get_by_id(user_id)

        if existing_user is not None:
            return existing_user
        
        raise utils.exceptions.UserNotFound(user_id)
    
    def get_user_events(self, user_id:int):

        self.get_user(user_id) #fetches the user
        
        event_ids = self.registration_repository.get_user_events(user_id)#fetches users events
        event_object_list = []
        
        for event_id in event_ids:
            event_object = self.event_repository.get_by_id(event_id)
            event_object_list.append(event_object)

        return event_object_list
        
