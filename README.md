Vantag Event Management System

A command-line event management application built with Python and SQLite, demonstrating clean architecture principles including separation of concerns, 
repository/service layering, and modular design.

Overview

Vantag is a fully functional CLI-based event management system that allows users to create, view, update, and delete events through an interactive menu interface. 
It was built as a structured learning project to apply real-world software design patterns in Python.

Features

- Create Events— Add new events with relevant details stored persistently
- View Events — List all events or look up specific records
- Update Events — Modify existing event information
- Delete Events— Remove events from the database
- Persistent Storage** — SQLite database with `pathlib`-based path management for portability
- Interactive Menu — Clean CLI navigation via a dedicated `MenuHandler` class

Project Structure
```
vantag-event-management/
│
├── main.py                  # Application entry point
├── menu_handler.py          # CLI menu logic and user interaction
│
├── repositories/
│   └── event_repository.py  # Database access layer (CRUD operations)
│
├── services/
│   └── event_service.py     # Business logic layer
│
├── models/
│   └── event.py             # Event data model
│
├── database/
│   └── db.py                # SQLite connection and schema setup
│
└── README.md

```
Architecture

```
This project follows a layered architecture pattern:

User Input (CLI)
      ↓
MenuHandler        ← handles all user interaction
      ↓
EventService       ← business logic, validation
      ↓
EventRepository    ← database queries (SQLite)
      ↓
SQLite Database

```
This separation ensures each component has a single responsibility, making the codebase easier to maintain, test, and extend.

 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core language |
| SQLite | Persistent local database |
| `pathlib` | Cross-platform file path handling |
| `sqlite3` | Standard library DB interface |

---

 Getting Started

 Prerequisites

- Python 3.8 or higher
- No external dependencies — uses Python standard library only

Installation

bash
# Clone the repository
git clone https://github.com/talented-toluwani/vantag-event-management.git

# Navigate into the project directory
cd vantag-event-management


Running the App

bash
python main.py


You'll be greeted with the interactive menu to start managing events.

---

Sample Interaction


============================
   VANTAG EVENT MANAGER
============================
1. Create Event
2. View All Events
3. Update Event
4. Delete Event
5. Exit

Enter your choice: 1

Event Name: Tech Summit 2025
Date: 2025-09-15
Location: Lagos, Nigeria
Description: Annual technology conference

Event created successfully!


Key Learnings

Building this project deepened my understanding of:

- Designing applications with separation of concerns in mind
- Implementing a repository pattern** to decouple database logic from business logic
- Using pathlib for robust, OS-independent file and database path handling
- Structuring a Python project for readability and future scalability
- Debugging real issues in a multi-layered codebase

---

 Potential Improvements

- [ ] Add user authentication and role-based access
- [ ] Migrate to a web interface using FastAPI + Jinja2
- [ ] Add event search and filtering by date or category
- [ ] Write unit tests for the service and repository layers
- [ ] Export event data to CSV or JSON



 Author
Toluwani Edgal
Software Engineering Student — Bowen University, Iwo, Nigeria
🔗 [GitHub Profile](https://github.com/talented-toluwani)

