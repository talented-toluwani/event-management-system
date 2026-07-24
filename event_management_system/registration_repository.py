import logging
from datetime import datetime

import event_exceptions as event_exceptions
from event_models import Event, User


class RegistrationRepository:
    def __init__(self,connection) -> None: # initializes a connection
        self.connection = connection


    def register(self, user_id: int, event_id: int) -> None:
        cursor = None
         
        if user_id is None:# checks if the user has a valid user id
            raise ValueError("User id is required!")
        
        if event_id is None:# checks if the user has a valid event id
            raise ValueError("Event id is required!")
        
        try:# fetches the users is from the table
            cursor = self.connection.cursor()
            sql_query_user = "SELECT COUNT(*) FROM users_table WHERE user_id = ?"
            cursor.execute(sql_query_user, (user_id,))
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                raise event_exceptions.UserNotFound(user_id)
            
            sql_query_event = "SELECT COUNT(*) from events_table WHERE event_id = ?"#fetches the users event id from the table
            cursor.execute(sql_query_event, (event_id,))
            event_count = cursor.fetchone()[0]

            if event_count == 0:
                raise event_exceptions.EventNotFound(event_id)
            
            """checks for duplicate registration, by first checking if the user has registered for any event before"""

            sql_query_duplicare_registration = "SELECT COUNT(*) from registrations_table WHERE user_id = ? and event_id = ?"
            cursor.execute(sql_query_duplicare_registration, ( user_id, event_id,))
            count_duplicate_registration = cursor.fetchone()[0]

            if count_duplicate_registration > 0:#checks if the user has registered before
                raise event_exceptions.DuplicateRegistration(user_id, event_id,)
            
            registered_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            sql_insert_query = "INSERT INTO registrations_table(user_id, event_id, registered_at) VALUES(?,?,?)"
            value = (user_id,
                     event_id,
                     registered_at,)
            
            cursor.execute(sql_insert_query, value)
            new_registration_id = cursor.lastrowid
            self.connection.commit()
            return new_registration_id
            
        except Exception:
            self.connection.rollback()
            logging.error(f"Failed to register user {user_id} for event {event_id}", exc_info= True)
            raise

        finally:
            if cursor is not None:
                cursor.close()


    def unregister(self, user_id: int, event_id:int) -> None:
        cursor = None

        if user_id is None:
            raise ValueError("User id is required!")
        
        if event_id is None:
            raise ValueError("Event id is required!")

        try:
            cursor = self.connection.cursor()    
            sql_query_1 = "DELETE FROM registrations_table WHERE user_id = ? and event_id = ?"
            cursor.execute(sql_query_1,(user_id, event_id,))
            
            if cursor.rowcount == 0:
                raise event_exceptions.NotRegistered(user_id, event_id)
            
            self.connection.commit()

        except event_exceptions.NotRegistered():
            raise

        except Exception:
            logging.error(
                f"Failed to unregister user with user id: {user_id}"
                f"from event with event id: {event_id}", exc_info= True)
            raise

        finally:
            if cursor is not None:
                cursor.close()


    def is_registered(self, user_id: int, event_id: int) ->  bool:
        cursor = None
         
        if user_id is None:
            raise ValueError("A valid user id is required to go further!")
        
        if event_id is None:
            raise ValueError("A valid event id is required to go further!")
        
        try:
            cursor = self.connection.cursor()

            query = "SELECT COUNT(*) FROM registrations_table WHERE user_id = ? and event_id = ?"
            cursor.execute(query, (user_id, event_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                return False

            return True

        except Exception:
            logging.error(
                f"Failed to verify if user with user id: {user_id} is registered "
                f"for event with event id: {event_id}", exc_info= True)
            raise
            
        finally:
            if cursor is not None:
                cursor.close()


    def get_user_events(self, user_id:int): 
        cursor = None

        if  user_id is None:
            raise ValueError("A valid user id is required to go further!")
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT event_id FROM registrations_table WHERE user_id = ?"
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return []
            
            return [row[0] for row in rows]

        except Exception:
            logging.error(f"An error occurred while trying to get all the event ids for user with {user_id} user id", exc_info = True)
            raise

        finally:
            if cursor is not None:
                cursor.close()  


    def get_events_participants(self, event_id: int):
        cursor = None
        
        if event_id is None:
            raise ValueError("A valid event id is required to go further")
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT user_id FROM registrations_table WHERE event_id = ?"
            cursor.execute(query, (event_id,))
            rows= cursor.fetchall()

            if not rows:
                return []
            
            return [row[0] for row in rows]

        except Exception:
            logging.error(f"An error occurred while trying to get all user ids for the event {event_id}", exc_info = True )
            raise

        finally:
            if cursor is not None:
                cursor.close()
        

