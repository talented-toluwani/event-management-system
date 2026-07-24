import logging
import sys

import event_config
from event_database import get_connection, init_database
from event_repository import EventRepository
from event_service import EventService
from menu_handler import MenuHandler
from registration_repository import RegistrationRepository
from user_repository import UserRepository
from user_service import UserService


def setup_logging():
    logging.basicConfig(
        level= getattr(logging, event_config.LOG_LEVEL),
        format= event_config.LOG_FORMAT
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