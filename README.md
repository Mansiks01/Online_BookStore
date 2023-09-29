# Online_BookStore

This is a Django-based web application for an online bookstore. It allows users to browse, search, and purchase books online. The project includes features such as user authentication, shopping cart, and a user profile system.

![Bookstore](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/Front.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Images](#images)

## Features

- **User Registration and Authentication**: Users can register and log in securely.
- **Browse Books by Category**: Books are categorized for easy browsing.
- **Search Books**: Users can search for books by title or author.
- **Shopping Cart**: Users can add books to their shopping cart.
- **User Profile Management**: Users can manage their profiles.
- **Admin Dashboard**: Admins can manage books and categories.
- **Responsive Design**: The app is responsive for mobile and desktop.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/Mansiks01/Online_BookStore.git



2. Navigate to the project directory:
    cd bookstore

3. Create a virtual environment (optional but recommended):

    python -m venv venv

4.  Activate the virtual environment:
    On Windows
    ```shell
    venv\Scripts\activate
    
 5. On macOS and Linux:
    ```shell
    source venv/bin/activate

6. Install the project dependencies:
      ```shell
    pip install -r requirements.txt


## Usage
1.  Apply database migrations:
    python manage.py migrate

2.  Create a superuser (admin account) to access the admin dashboard:

    python manage.py createsuperuser

3.  Start the development server:

    python manage.py runserver

4. Open a web browser and navigate to http://localhost:8000 to access the application.   


## Configuration
1. In Settings.py :
    Fill:   EMAIL_HOST_USER = ''
            EMAIL_HOST_PASSWORD = '' 
    these with your email and password
2. In my.cnf :
    Fill:
    name of database, user and password

 ## Images
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/Detail%20page.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/add%20to%20cart%20option.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/Pagination.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/add%20to%20cart%20option.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/empty%20cart.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/forget%20password.png)
 ![Detail](https://github.com/Mansiks01/Online_BookStore/blob/main/Screenshots/Cart%20page.png)
