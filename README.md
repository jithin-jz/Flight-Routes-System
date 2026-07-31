# Flight Routes System

**GitHub Repository**: [https://github.com/jithin-jz/Flight-Routes-System](https://github.com/jithin-jz/Flight-Routes-System)

A Django web application designed to manage, traverse, and analyze binary tree flight route networks between airport nodes using a clean, minimal light Bootstrap interface.

---

## Table of Contents

- [Overview](#overview)
- [Key Features & Questions Addressed](#key-features--questions-addressed)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Prerequisites](#prerequisites)
- [Local Setup & Installation](#local-setup--installation)
- [Running the Development Server](#running-the-development-server)
- [Running Automated Unit Tests](#running-automated-unit-tests)
- [Database Configuration](#database-configuration)

---

## Overview

The **Flight Routes System** models airport networks as a **Binary Tree** where each `Airport` node maintains:
- `code`: Unique airport code (e.g. `JFK`, `DXB`, `DEL`).
- `duration`: Flight/stay duration in minutes.
- `left`: Pointer to the left child airport node.
- `right`: Pointer to the right child airport node.

---

## Key Features & Questions Addressed

1. **Add Airport Route Form**:
   - Create new root nodes or attach child nodes (`Left` or `Right`) to an existing parent node.
   - Form validation ensures unique airport codes, auto-uppercases inputs, and prevents attaching nodes to occupied child positions.

2. **Q1: Directional Search Traversal (Last Reachable Node)**:
   - Select any starting airport node from a dropdown and choose a traversal direction (`Left` or `Right`).
   - Continuously traverses down the binary tree in the chosen direction until reaching the last reachable airport node.

3. **Q2: Longest Duration Airport**:
   - Identifies and displays the airport node with the highest duration value (`Airport.objects.order_by('-duration').first()`).

4. **Q3: Shortest Duration Airport**:
   - Identifies and displays the airport node with the lowest duration value (`Airport.objects.order_by('duration').first()`).

5. **One-Page Minimal Light Dashboard**:
   - Combines binary tree visualizer, in-page form panels, airport registry table, and path highlighting on a clean, minimal light Bootstrap 5 dashboard (`/`).
   - Individual standalone routes (`/add/`, `/search/`, `/longest/`, `/shortest/`) remain fully functional.

---

## Technology Stack

- **Backend**: Python 3.12, Django 6.0.7
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Bootstrap 5.3, Bootstrap Icons
- **Design Theme**: Minimal Light Interface

---

## Project Architecture

```
flight_routes/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── flight_routes_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── routes/
│   ├── models.py       # Airport binary tree model
│   ├── forms.py        # AddAirportForm & SearchForm with validations
│   ├── views.py        # One-page controller & individual route views
│   ├── urls.py         # Application routing
│   ├── admin.py        # Django Admin integration
│   └── tests.py        # 17 automated unit tests
└── templates/
    └── routes/
        ├── base.html        # Main layout & minimal light theme design
        ├── home.html        # One-Page Dashboard & tree visualizer
        ├── add_airport.html # Standalone Add Airport page
        ├── search.html      # Standalone Search page
        ├── longest.html     # Standalone Longest Duration page
        └── shortest.html    # Standalone Shortest Duration page
```

---

## Prerequisites

- **Python**: Version 3.10 or higher
- **pip**: Python package manager

---

## Local Setup & Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/jithin-jz/Flight-Routes-System.git
   cd flight_routes
   ```

2. **Create and Activate a Virtual Environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

---

## Running the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Add Airport Page**: [http://127.0.0.1:8000/add/](http://127.0.0.1:8000/add/)
- **Search Traversal Page**: [http://127.0.0.1:8000/search/](http://127.0.0.1:8000/search/)
- **Longest Duration Page**: [http://127.0.0.1:8000/longest/](http://127.0.0.1:8000/longest/)
- **Shortest Duration Page**: [http://127.0.0.1:8000/shortest/](http://127.0.0.1:8000/shortest/)
- **Admin Interface**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Running Automated Unit Tests

Run the complete test suite (17 tests):
```bash
python manage.py test
```

Expected Output:
```text
Creating test database for alias 'default'...
.................
----------------------------------------------------------------------
Ran 17 tests in 0.079s

OK
Destroying test database for alias 'default'...
```

Run Django system check:
```bash
python manage.py check
```

---

## Code Formatting & Linting

Format codebase using Black & Ruff:
```bash
black .
ruff format .
ruff check . --fix
```

---

## Database Configuration

The application uses **SQLite** as its default database backend configured in `flight_routes_project/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```
