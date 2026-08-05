import logging

logger = logging.getLogger(__name__)

from datetime import datetime, timezone

from models.enums import EventCategory, EventStatus
from models.models import Event
from utils.exceptions import EventNotFound


class EventRepository:
      def __init__(self, connection) : #initializes with the connection object
            self.connection = connection #this is a databse connection, prevents every object from creating its own connection
      
      def create(self, event: Event) :
           cursor = None
           #inserting a new event into the database
           database = ("""INSERT INTO events_table(
                     title,description, date_time, max_capacity, category,current_participants, status)
                     VALUES (?,?,?,?,?,?,?)""") #this is the event object 
           
           data = (event.title,
                event.description,
                event.date_time.strftime("%Y-%m-%d %H:%M"), 
                event.max_capacity, 
                event.category.value, 
                event.current_participants,
                event.status.value) #these are the values to be inserted into the event object, and they are data values
           
           try:
                cursor = self.connection.cursor() #creates a cursor object

                cursor.execute(database, data)
      
                new_id = cursor.lastrowid #returning the unique event id

                self.connection.commit()

                event.event_id = new_id


           except Exception:
                self.connection.rollback()
                logger.error("An error occurres in the create method")
                raise
           
           finally:
                 if cursor is not None:
                    cursor.close()
            
           return event

      def get_by_id(self, event_id: int):
           cursor = None
           
           try:
               query = "SELECT * FROM events_table WHERE event_id = ?" #fetches data only from row, where the id will be provide
               cursor = self.connection.cursor()
               cursor.execute(query, (event_id,)) # the event is made a tuple, and it is passed into the query
               row = cursor.fetchone()#returns a match if it finds similar event, if not none, and helps it to hold actual data.
            
               if row is not None: #validates if there are any data stored in my_row
                return self._row_to_event(row) #a function call for the helper function
               
           except EventNotFound:
               logger.exception("The event to be fetched was not gotten")
               raise 


           finally:
                if  cursor is not None:
                 cursor.close()

      def _row_to_event(self, row):
          
            """
            internal or helper function that convets row to event object
            """
            date_time = datetime.strptime(row[3], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)#convertes data time stored as string
            return Event(
                event_id= row[0],
                title = row[1],
                description = row[2],
                date_time= date_time,
                max_capacity= int(row[4]),
                category= EventCategory(row[5]),
                current_participants= int(row[6]),
                status= EventStatus(row[7])) # does data extraction by mapping  the event object to an id
      
      def get_all_events(self): #fetches all the event ordered by date
           cursor = None
           try:
                query = "SELECT * FROM events_table ORDER BY date_time  "
                cursor = self.connection.cursor()
                cursor.execute(query)

                rows = cursor.fetchall() #fetches all the rows in the table
                events_lists = []#makes an empty list to add the event object to 
                
                for row in rows: #loops through each rows 
                    event_object = self._row_to_event(row)#calls the helper function which converts the rows to event objects
                    events_lists.append(event_object) #adds the event to the list
                return events_lists #returns the complete list
            
           except Exception: #this is what happens incase an error exists 
                 logger.exception("An error occurred in get_all")
                 raise 

           finally: #closes the cursor
                 if  cursor is not None:
                    cursor.close()

      def get_events_by_user(self, user_id):
          cursor = None

          try:
              query = """SELECT e.* FROM events_table e
                        INNER JOIN registrations_table r ON e.event_id = r.event_id
                        WHERE r.user_id = ?
                        ORDER BY e.date_time   
              """
              cursor = self.connection.cursor()
              cursor.execute(query, (user_id,))

              rows = cursor.fetchall()
              event_list = []

              for row in rows:
                  event_object = self._row_to_event(row)
                  event_list.append(event_object)
              return event_list
            
          except Exception:
              logger.error("Error in get_events_by_user")
              raise
          
          finally:
              if cursor is not None:
                  cursor.close()
                  

      def get_upcoming(self):#fetches all the events, filtered by date and status
           cursor = None
           try:
                cursor = self.connection.cursor()#establieshes a cursor object
                query = "SELECT * FROM events_table WHERE status = 'upcoming'"
                cursor.execute(query)

                rows = cursor.fetchall() #fetches all the rows that matches the query
                event_upcoming_list = [] #an empty list to store the upcoming events objects

                for row in rows:#loops over individual items 
                    event_upcoming_object = self._row_to_event(row)
                    event_upcoming_list.append(event_upcoming_object)
                return event_upcoming_list
           
           except Exception :#prints an error message, if an error is encountered
                logger.exception("An error occurred in get_upcoming")
                return []
           
           finally: #closes the cursor 
                if  cursor is not None:
                   cursor.close()


      def search(self,keyword):
        cursor = None
        try:
            cursor = self.connection.cursor()
            keyword =  f"%{keyword}%"
            query = "SELECT * FROM events_table WHERE title LIKE ?  OR description LIKE ? "
            cursor.execute(query, (keyword,keyword,))
            rows = cursor.fetchall()
            search_lists = []
            for row in rows:
                event_search_object = self._row_to_event(row)
                search_lists.append(event_search_object)
            return search_lists
        
        except Exception:
            logger.exception("An error occurred in search")
            return []

        finally:
            if cursor is not None:
                cursor.close()

      def get_by_category(self, category):
          cursor = None
          try:
              cursor = self.connection.cursor()
              new_category = category.value #raw value of category
              query = "SELECT * FROM events_table WHERE category = ?"
              cursor.execute(query, (new_category,))
              rows = cursor.fetchall()
              category_list = []
              for row in rows:
                category_object = self._row_to_event(row)
                category_list.append(category_object)
              return category_list
          
          except Exception:
              logger.exception("An error occurred in get_by_category")
              return []

          finally:
              if cursor is not None:
                  cursor.close()

      def update(self, event: Event):
          cursor = None
    
          try:
              cursor = self.connection.cursor()
              event_id = event.event_id #extracts the event_id

              if event_id is None:
                return None

              sql_query = "SELECT COUNT(*) FROM events_table WHERE event_id = ?"
              cursor.execute(sql_query, (event_id,))
              count = cursor.fetchone()[0] #checks,and fetches the event_id

              if count == 0:
                   return None

              new_extracted_values = ( event.title,
                    event.description,
                    event.date_time.strftime("%Y-%m-%d %H:%M"),
                    event.max_capacity,
                    event.category.value,
                    event.current_participants,
                    event.status.value, 
                    event_id)  #fetches the event details to be updated
                
              query = """UPDATE events_table SET
                title = ?,
                description = ?,
                date_time = ?,
                max_capacity= ?,
                category = ?,
                current_participants = ?,
                status = ?
                WHERE event_id = ?
            """
              
              cursor.execute(query, new_extracted_values)
              self.connection.commit()
              return event
          
          except Exception:
              logger.error("An error occurred in update")
              raise

          finally:
              if cursor is not None:
                  cursor.close()
                  
      def delete(self, event_id:int):
          cursor = None

          try:
              cursor = self.connection.cursor() 
            
              if event_id is None:
                  return None
                
              sql_query =  "SELECT COUNT(*) FROM events_table WHERE event_id = ?"
              cursor.execute(sql_query, (event_id,))
              count = cursor.fetchone()[0]

              if count == 0:
                  return None
               
              query = ("DELETE FROM events_table WHERE event_id = ?")
              cursor.execute(query, (event_id,))
              self.connection.commit()
              return True 
          
          except Exception:
              logger.error("An error occurred in delete")
              raise

          finally:
              if cursor is not None:
                  cursor.close()
              
          
      def get_participant_count(self, event_id:int):
          cursor = None

          try:
              cursor = self.connection.cursor()

              sql_query = "SELECT COUNT(*) FROM registrations_table WHERE event_id = ?"
              cursor.execute(sql_query, (event_id,))
              count = cursor.fetchone()[0]

              return count

          except Exception:
              logger.exception("An error occurred in get_participant_count")
              raise
              
          finally:
              if cursor is not None:
                  cursor.close()
              
          
