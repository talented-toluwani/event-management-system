import logging 
import event_exceptions
from event_enums import UserRole, EventCategory, EventStatus
from event_config import DISPLAY_DATE_FORMAT, DATE_FORMAT
from datetime import datetime

class MenuHandler:

    def __init__(self, user_service, event_service,  registration_repository):

        self.event_service = event_service
        self.user_service = user_service
        self.registration_repository = registration_repository
        self.current_user = None 
        self.logger = logging.getLogger(__name__)
    

    def run(self):
        print("------ Welcome to Vantag Event Management System ------")
        
        while True:

            if self.current_user is None:
                should_continue = self.handle_main_menu()
                if not should_continue:
                    break

            elif self.current_user.role == UserRole.PARTICIPANT.value:
                should_continue = self.handle_participant_menu()
                if not should_continue:
                    break

            elif self.current_user.role == UserRole.ADMIN.value:
                should_continue = self.handle_admin_menu()
                if not should_continue:
                    break

        print("------ Thanks for making use of the event management system. Enjoy your booked event(s)! ------")
    

    def handle_main_menu(self):
        print ("\n--- Welcome to the main menu of the Vantag Event Management System! ---")

        print("You can perform these following actions: \n")

        print("1. Register as a new user.")
        print("2. Login.")
        print("3. Exit.")

        user_choice = self._get_menu_choice(1,3)
        
        if user_choice == 1:
            self._register_new_user()
            return True

        elif user_choice == 2:
            self._login()
            return True
        
        else:
            return False
        
    
    def handle_participant_menu(self):
        print(f"\n === Welcome {self.current_user.name} to the participant menu of the Vantag Event Management System === ")
        print("You can perform the following actions:\n")
        
        print("1. View all events")
        print("2. View upcoming events")
        print("3. Search events")
        print("4. Join event")
        print("5. Cancel registration")
        print("6. View my registered events ")
        print("7. Logout")
        
        user_choice = self._get_menu_choice(1,7)
        
        if user_choice == 1:
            self._view_all_events()
            return True
        
        elif user_choice == 2:
            self._view_upcoming_events()
            return True
        
        elif user_choice == 3:
            self._search_events()
            return True
        
        elif user_choice == 4:
            self._join_event()
            return True
        
        elif user_choice == 5:
            self._cancel_registration()
            return True
        
        elif user_choice == 6:
            self._view_my_events()
            return True
        
        elif user_choice == 7:
            self._logout()
            return True
        
    
    def handle_admin_menu(self):
        print(f"\n === Welcome {self.current_user.name} to the Admin Menu of the Vantag Event Management System")
        print("You can perform the following actions.\n")

        print("1. Create event")
        print("2. View all events")
        print("3. Edit event")
        print("4. Cancel event")
        print("5. Delete event")
        print("6. View event participants")
        print("7. View upcoming events")
        print("8. Search events")
        print("9. Logout")

        user_choice = self._get_menu_choice(1,9)
              
        if user_choice == 1:
            self._create_event()
            return True
        
        elif user_choice == 2:
            self._view_all_events()
            return True
        
        elif user_choice == 3:
            self._edit_event()
            return True
        
        elif user_choice == 4:
            self._cancel_event_admin()
            return True

        elif user_choice == 5:
            self._delete_event()
            return True
        
        elif user_choice == 6:
            self._view_event_participants()
            return True
        
        elif user_choice == 7:
            self._view_upcoming_events()
            return True
        
        elif user_choice == 8:
            self._search_events()
            return True
        
        elif user_choice == 9:
            self._logout()
            return True
        

    def _register_new_user(self):
        print("\n === Register New User === ")

        user_name = self._get_string_input("Enter in your name: ")
        user_email = self._get_string_input("Enter in your valid email: ")
        
        print("Select your role")
        print("1. Participant")
        print("2. Admin")

        user_choice = self._get_menu_choice(1,2)
        
        user_role = None
        
        role_map = {1: UserRole.PARTICIPANT, 2:UserRole.ADMIN}
        user_role = role_map.get(user_choice)

        try:
            new_user = self.user_service.register_user(user_name, user_email, user_role)

            if new_user is None:
                print("Failed to create user...")

            else:
                print(f"Registration successful! Welcome {new_user.name}.")
                self.current_user = new_user

        except event_exceptions.InvalidEmail as e:
            print(f"Error message: {e}")
            self.logger.error("The user entered in an invalid email format", exc_info=True)
          
        except event_exceptions.DuplicateRegistration as e:
            print(f"Error message: {e}")
            self.logger.error("The user has registered before.", exc_info=True)
            
                
        except ValueError as e:
            print(f"Invalid input: {e}")
            self.logger.error("The users entered in a wrong input")
            
        except Exception as e:
            print("An unexpected error occurred. Please try again.")
            self.logger.error(f"Unexpected error occurred {e}")


    def _login(self):
        print("\n === Login === ")
        email = self._get_string_input("Enter in your email: ") #gets the user's email

        try:
            user = self.user_service.login(email.lower()) #logs in the user

            if user is None:
                print(f"No user found with this {email} email.")
                print("Tip: Register as a new user from the main menu.")

            else:
                self.current_user = user
                print("Welcome back. Login successful!")

        except Exception as e:
            self.logger.error(f"Login error {e}")
            print("An error occurred while trying to log in. Please, try again.")

    def _logout(self):
        if self.current_user is not None:
            print(f"Goodbye {self.current_user.name}!")

            self.current_user = None
            print("You have succesfull logged out.")

    def _view_all_events(self):
        print("\n === All events === ")

        try:
            events = self.event_service.get_all_events()
              
            if not events:
                print("Sorry, no events available presently.")
                return #exists the method if there are no availabe events
            
            self._display_events_list(events)
               
        except Exception as e:
            self.logger.error(f"Error occurred: {e}", exc_info = True)
            print("Failed to load events. Please try again.")

    def _view_upcoming_events(self):
        print("\n === Upcoming Events === ")

        try:
            events = self.event_service.get_upcoming_events()

            if not events:
                print("No upcoming events available.")
                return
            
            self._display_events_list(events)

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to load upcoming events. Please try again.")

    def _search_events(self):
        print("\n === Search Events === ")

        keyword = self._get_string_input("Enter search keyword: ")

        try:
            events = self.event_service.search_events(keyword)

            if not events:
                print(f"No event found matching {keyword}")
                return
            
            else:
                print(f"Found {len(events)} event(s) matching {keyword} ")
                self._display_events_list(events)

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Search failed. Please try again.")

    def _view_my_events(self):
        print("\n === My Registered Events === ")
        
        try:
            events = self.event_service.get_events_by_user(self.current_user.user_id)
            
            if not events:
                print("You are yet to register for any events.")
                print("Tip: Use 'Join event' to register for events.")
                return
            
            print(f"You are registered for {len(events)} event(s)")
            self._display_events_list(events)

        except event_exceptions.UserNotFound as e:
            self.logger.error("User was not found")
            print(f"Error ocurred: {e}")

        except Exception as e:
            self.logger.error(f"Error viewing user events: {e}")
            print("Failed to load your events. Please try again.")


    def _join_event(self):
        print("\n === Join Event === ")      
        print("Available Events: ")

        try:
            events = self.event_service.get_upcoming_events()

            if not events:
                print("No upcoming events available to join.")
                return
            
            self._display_events_list(events)

            event_id = self._get_integer_input("Enter event ID to join.")

            self.event_service.register_user(self.current_user.user_id, event_id)
            print("Successfully registered for the event!")
            print("You can view your registered events from the main menu.")
        
        except event_exceptions.EventFullError as e:
            self.logger.error(f"Error occurred: {e}")
            print("This event is at full capacity. Please choose another event.")

        except event_exceptions.DuplicateRegistration as e:
            self.logger.error(f"Error occurred: {e}")
            print("You are already registered for this event.")

        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("No event with the event id found.")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to join event. Please try again.")

    def _cancel_registration(self):
        print("\n === Cancel Registration === ") 
        print("Your registered events: ")

        try:
            events = self.event_service.get_events_by_user(self.current_user.user_id)

            if not events:
                print("You have not registered for any events.")
                return
            
            self._display_events_list(events)

            event_id = self._get_integer_input("Enter event ID to cancel.")
            confirmed = self._get_confirmation("Are you sure you want to cancel this regsitration? (yes/no: ")

            if not confirmed:
                print("Cancellation aborted.")
                return
        
            self.event_service.unregister_user(self.current_user.user_id, event_id)
            print("Registration cancelled successfully.")

        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("Event was not found.")

        except Exception as e:
            self.logger.error(f"Error cancelling event: {e}")
            print("Failed to cancel registration. Please try again.")

    
    def _create_event(self):
        print("\n === Create New Event === ")

        title = self._get_string_input("Enter event title: ")
        description = self._get_string_input("Enter event description: ")
        date_time = self._get_datetime_input("Enter event date and time (YYYY-MM-DD HH:MM): ")
        max_capacity = self._get_integer_input("Enter maximum capacity: ")

        if max_capacity <= 0:
            print("Capacity must be greater than 0")
            return
        
        print("\n Select Event Category: ")
        print(f"1. {EventCategory.WORKSHOP.value}")
        print(f"2. {EventCategory.SEMINAR.value}")
        print(f"3. {EventCategory.SPORTS.value}")
        print(f"4. {EventCategory.OTHER.value}")

        user_choice = self._get_menu_choice(1, 4)
        
        category_map = {
            1: EventCategory.WORKSHOP,
            2: EventCategory.SEMINAR,
            3: EventCategory.SPORTS,
            4: EventCategory.OTHER
        }
        
        category = category_map[user_choice]
       
        try:
            new_event = self.event_service.create_event(title, description, date_time, max_capacity, category)
            print(f"Success! Event {new_event.title} created successfully!")
            print(f"Event ID {new_event.event_id}")

        except event_exceptions.InvalidDate as e:
            self.logger.error(f"Error occurred: {e}")
            print("Event must be scheduled for future dates.")

        except ValueError as e:
            self.logger.error(f"Error occurred: {e}")
            print("Invalid input. Please ensure valid data was supplied for each required field.")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to create event. Please try again.")
        
  
    def _edit_event(self):

        print("\n === Edit Event === ")

        self._view_all_events()
        event_id = self._get_integer_input("Enter event ID to edit: ")

        try:
            event = self.event_service.get_event(event_id)

        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("No event found.")
            return
        
        print("\n Current event details")
        self._display_single_event(event)

        print("\n What will you like to edit?")

        print("1. Title")
        print("2. Description")
        print("3. Date and Time ")
        print("4. Maximum Capacity")
        print("5. Category")
        print("6. Cancel")

        user_choice = self._get_menu_choice(1, 6)

        if user_choice == 1:

            new_title = self._get_string_input("Enter new title: ")
            event.title = new_title

        elif user_choice == 2:

            new_description = self._get_string_input("Enter new description: ")
            event.description = new_description

        elif user_choice == 3:
            
            new_date_time = self._get_datetime_input("Enter new date and time (YYYY-MM-DD HH:MM): ")
            event.date_time = new_date_time

        elif user_choice == 4:

            new_capacity = self._get_integer_input("Enter new maximum capacity: ")

            if new_capacity > 0:
                event.max_capacity = new_capacity
            else:
                print("New capacity must be greater than 0")
                return

        elif user_choice == 5:

            print("\n Select Event Category: ")
            print(f"1. {EventCategory.WORKSHOP.value}")
            print(f"2. {EventCategory.SEMINAR.value}")
            print(f"3. {EventCategory.SPORTS.value}")
            print(f"4. {EventCategory.OTHER.value}")

            category_choice = self._get_menu_choice(1, 4)

            category_map = {
            1: EventCategory.WORKSHOP,
            2: EventCategory.SEMINAR,
            3: EventCategory.SPORTS,
            4: EventCategory.OTHER
        }    
            event.category = category_map[category_choice]
        
        else:
            return
        
        try:
            self.event_service.update_event(event)
            print("Event updated successfully")

        except event_exceptions.InvalidDate as e:
            self.logger.error(f"Error occurred: {e}")
            print("Invalid date.")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to edit event. Please try again!")

    def _cancel_event_admin(self):

        print("\n === Cancel Event === ")
        self._view_all_events()

        event_id = self._get_integer_input("Enter event ID to cancel: ")
        confirmed = self._get_confirmation("Are you sure you want to cancel this event? This will notify alll registered users(yes/no): ")

        if not confirmed:
            print("Action aborted")
            return

        try:
            self.event_service.cancel_event(event_id)
            print("Event cancelled successfully!")
            print(f"Status changed to {EventStatus.CANCELLED.value}")

        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("Event not found")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to cancel event.")

    def _delete_event(self):

        print("\n === Delete Event ===")
        self._view_all_events()
        event_id = self._get_integer_input("Enter event ID to delete: ")

        print("WARNING: This will permanently delete the event and all registrations.")
        print("This action CANNOT be undone.")
        confirmed = self._get_string_input(" Type 'DELETE' to confirm: ").upper()

        if confirmed != "DELETE":
            print("Deletion Cancelled.")
            return
        
        try:
            self.event_service.delete_event(event_id)
            print("Event deleted permanently.")

        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to delete event.")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to delete event.")

    def _view_event_participants(self):

        print("\n === View Event Participants ===")
        self._view_all_events()
        event_id = self._get_integer_input("Enter event ID to view participants.")

        try:
            event = self.event_service.get_event(event_id)
            print("\nEvent Details:")
            print(f"Event: {event.title}")
            formatted_date = event.date_time.strftime(DISPLAY_DATE_FORMAT)
            print(f"Date: {formatted_date}")
            print(f"Capacity: {event.current_participants}/{event.max_capacity}")
        
        except event_exceptions.EventNotFound as e:
            self.logger.error(f"Error occurred: {e}")
            print("Event not found.")
            return

        try:
            participant_ids = self.registration_repository.get_event_participants(event_id)

            if not participant_ids:
                print("No participants for this event.")
                return
            
            print(f"\n Registered participants {len(participant_ids)}")
            for index, user_id in enumerate(participant_ids, start = 1):
                user = self.user_service.get_user(user_id)
                print(f"{index}. {user.name} ({user.email}) - Role: {user.role.value}")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            print("Failed to load participants.")

    
    def _display_events_list(self, events):
        print("=" * 80)

        for event in events:
            self._display_single_event(event)
            print("-" * 80)
        
        print("=" * 80)
    

    def _display_single_event(self, event ):

        formatted_date = event.date_time.strftime(DISPLAY_DATE_FORMAT)
        available = event.available_spots
        
        if event.is_full:
           status_text = "FULL"
           print(status_text)
        
        elif event.status == EventStatus.CANCELLED:
            status_text ="CANCELLED"
            print(status_text)
        
        else:      
            status_text = event.status.value
            print(status_text)

        print("\n Below are the complete event details: ")

        print(f"Event ID: {event.event_id}")
        print(f"Title: {event.title} ")
        print(f"Description: {event.description}")
        print(f"Category: {event.category.value}")
        print(f"Date & Time: {formatted_date}")
        print(f"Capacity: : {event.current_participants} / {event.max_capacity}")
        print(f"Available_spots: {available}")
        print(f"Status: {status_text} ")

        if event.is_full:
            print("🔴 This event is full")

        elif available < 5:
            print(f"⚠️ Only {available} spots remaining!")

    def _get_menu_choice(self, min_choice, max_choice):

        while True:
            user_choice = self._get_integer_input(f"Enter your choice in this order ({min_choice}-{max_choice}):  ")

            if (user_choice < min_choice) or (user_choice > max_choice):
                print(f"Invalid choice. Please enter a number between {min_choice} and {max_choice}")
                continue
            return user_choice
            
    
    def _get_integer_input(self, prompt):
        while True:
            try:
                user_input = input(prompt).strip()
                converted_input = int(user_input)
                return converted_input
            
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                
    def _get_string_input(self, prompt):
        while True:
           
            user_input = input(prompt).strip()
           

            if not user_input:
                print("Input cannot be empty. Please try again.")
                continue

            return user_input
        
    def _get_datetime_input(self, prompt):
        while True:
            try:
                user_input = input(prompt).strip()
                datetime_object = datetime.strptime(user_input, DATE_FORMAT)
                return datetime_object

            except ValueError:
                print( "Invalid date format. Please use YYYY-MM-DD HH:MM")
                print("Example: 2025-12-25 18:30")
                continue
    
    def _get_confirmation(self, prompt):
        while True:
            user_response = input(prompt).strip().lower()

            if user_response not in ["yes", "no"]:
                print("Invalid input. Please enter yes or no.")
                continue

            elif user_response == "yes":
                return True
            
            else:
                return False