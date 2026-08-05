import logging

from database.connection import get_connection
from database.event_repo import EventRepository

connection = get_connection()

event_repo = EventRepository(connection) #this connects my event repository clas to my pre made event database file

logging.basicConfig(level = logging.DEBUG, format =' %(asctime)s - %(levelname)s - %(message)s' )