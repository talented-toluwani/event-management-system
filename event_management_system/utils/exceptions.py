class EventSystemError(Exception):
    pass

class EventFullError(EventSystemError):
    """raises a custom error message is the maximum capacity for an event has been reached"""
    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id
        message = "The event has reached its maximum capacity. No more participants are accepted."
        super().__init__(message)
    
class DuplicateRegistration(EventSystemError):
     """"raises a custom error meesage is a user who has registered to for an event wants 
     to re register"""
     def __init__(self, user_id, event_id):
          self.user_id = user_id
          self.event_id = event_id
          message = "Sorry. Participants can only register once." #custom error message to be displayed
          super().__init__(message)

class EventNotFound(EventSystemError):
     """raises a custom made error if an event is not found"""
     def __init__(self, event_id):
          self.event_id = event_id
          message = "Oops! Event not found. Please, ensure you typed in entered the right information." 
          super().__init__(message)

class UserNotFound(EventSystemError):
     """raises a custom error messsage if a user was not found"""
     def __init__(self,user_id):
          self.user_id = user_id
          message = "Sorry, user not found. Please, ensure that you entered in the right information"
          super().__init__(message)

class InvalidDate(EventSystemError):
     """"raises a custom error message if an invalid date value was enetered"""
     def __init__(self, date_value):
          self.date_value = date_value
          message = "Oops! Invalid date."
          super().__init__(message)

class InvalidEmail(EventSystemError):
     """raises a custom error message if a user has an invalid email"""
     def __init__(self, email):
          self.email = email
          message = "Invalid email address. Please ensure that the right information is entered"
          super().__init__(message)

class NotRegistered(EventSystemError):
     """raises a custom error message if a user is not registered for a particular event"""
     def __init__(self, user_id, event_id):
          self.user_id = user_id
          self.event_id = event_id
          message = f"The user {user_id} is not registered for the event {event_id}"
          super().__init__(message)

class EventAlreadyCancelled(EventSystemError):
     def __init__(self, event_id):
          self.event_id = event_id
          message = f"Event with event id {event_id} has already been cancelled."
          super().__init__(message)

