# Online_BookStore
# Bookstore Web Application

![Bookstore]

This is a Django-based web application for an online bookstore. It allows users to browse, search, and purchase books online. The project includes features such as user authentication, shopping cart, and a user profile system.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Use](#use)


## Features

- User Registration and Authentication
- Browse Books by Category
- Search Books by Title or Author
- Add Books to the Shopping Cart
- Change User Password
- User Profile Management
- Admin Dashboard for Managing Books and Categories
- Responsive Design for Mobile and Desktop

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/Mansiks01/Online_BookStore.git


2. Navigate to the project directory:
    cd bookstore

3. Create a virtual environment (optional but recommended):

    python -m venv venv

4.  Activate the virtual environment:

    On Windows:
    venv\Scripts\activate
    On macOS and Linux:
    source venv/bin/activate

5.  Install the project dependencies:
    pip install -r requirements.txt

## Use
1.  Apply database migrations:
    python manage.py migrate

2.  Create a superuser (admin account) to access the admin dashboard:

    python manage.py createsuperuser

3.  Start the development server:

    python manage.py runserver

4. Open a web browser and navigate to http://localhost:8000 to access the application.   
