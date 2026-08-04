import logging
import sys

import data.config
from database.connection import get_connection, init_database
from database.event_repo import EventRepository
from database.registration_repo import RegistrationRepository
from database.user_repo import UserRepository
from services.event_service import EventService
from services.user_service import UserService
from ui.menu import MenuHandler


def setup_logging():
    logging.basicConfig(
        level= getattr(logging, data.config.LOG_LEVEL),
        format= data.config.LOG_FORMAT
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Application logging initialized.")


def initialize_database():
    logger = logging.getLogger(__name__)
    logger.info("Initializing database.")
    init_database()
    logger.info("Database initialized successfully.")


def create_repositories(connection):
    logger = logging.getLogger(__name__)
    logger.info("Creating repository instances.")
    
    user_repository = UserRepository(connection)
    event_repository = EventRepository(connection)
    registration_repository = RegistrationRepository(connection)

    logger.info("Repository instances created successfully.")

    return user_repository, event_repository, registration_repository

def create_services(user_repository, event_repository, registration_repository):
    logger = logging.getLogger(__name__)
    logger.info("Creating services instance,")

    user_service = UserService(user_repository,event_repository,registration_repository)
    event_service = EventService(event_repository, registration_repository)

    logger.info("Services instance successfully created.")
    return(user_service, event_service)
    

def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting Event Management System.")

    try:
        initialize_database()
        connection = get_connection()
        user_repository, event_repository, registration_repository = create_repositories(connection)
        user_service, event_service = create_services(user_repository, event_repository, registration_repository)
        menu = MenuHandler(user_service, event_service, registration_repository)

        logger.info("Application initialized successfully.")
        logger.info("Starting user interface...")
        menu.run()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
        print("\n\n Application terminated by user. Goodbye!")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print("An error occurred. Please check logs for details.")
        sys.exit(1)

    finally:

        if 'connection' in locals() and connection:
            connection.close()
            logger.info("Database connection closed")
    
   
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()