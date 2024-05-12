# TaskManagerFlask

## Overview
TaskManagerFlask is a simple yet comprehensive web application built using Flask and Bootstrap designed to help users efficiently manage their daily tasks. The application facilitates task addition, updates, deletion, and completion marking. It also features robust user authentication, profile management, and dynamic task filtering based on due dates.

## Features
- **User Authentication**: Includes user profile registration (Signup), Login, and Logout functionalities.
- **Task Management**: Enables users to Add, Update, Delete, and Mark tasks as Completed.
- **Profile Management**: Enables users to Edit their profiles and Reset their passwords.
- **Task Filtering**: Provides various filters for tasks including All, Pending, Today, Expired, Upcoming, and Completed.
- **Email Notifications**: Sends automated notifications for Account Confirmation and Password Resets, enhancing account security.

## Technologies Used
- **Flask**: Utilized as the core web application framework to manage routing, requests, and the app's server-side logic.
- **Flask-Login**: Handles user authentication processes, session management, and access control, making it easier to manage user-specific data securely.
- **Flask-Mail**: Facilitates direct email sending from the application, crucial for implementing features like account verification and password recovery.
- **Flask-WTF**: Integrates Flask applications with WTForms to handle form creation, rendering, and validation, simplifying HTML forms management.
- **Flask-SQLAlchemy**: Acts as the ORM layer; simplifies database operations by providing an abstraction layer to manipulate the database with Python code instead of SQL.
- **SQLite**:  Chosen for its simplicity and efficiency in managing lighter, disk-based databases, perfect for small to medium applications.
- **Bootstrap**: Enhances the front-end framework for creating responsive and mobile-first web pages, ensuring a consistent and professional look across various devices.
- **Javascript**: Used for dynamically displaying flash messages and implementing task filtering without reloading the page.
- **pytest**: Ensures the robustness of the application by enabling comprehensive testing frameworks to write and execute automated tests.

## Installation 
### Prerequisites
- Python 3
- pip
- Virtualenv (optional)

## Setup
1. Clone the repository:
```
git clone https://github.com/yourusername/TaskManagerFlask.git
cd TaskManagerFlask
```
2. Create a virtual environment (optional):
```
python -m venv venv
# On Linux and MacOs:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Create a `.env` file based on the example provided in the `.env.example` and update it with your database credentials and secret key.
5. Run the application:
```
python run.py
```

## Usage
Once the application is running, navigate to http://127.0.0.1:5000/ in your web browser to start using TaskManagerFlask. Register a new user or login with existing credentials to manage tasks.

## Testing
To run the tests for the application, execute:
```
pytest
```

## Contributing
This project is for my web development portfolio designed to showcase development skills and is not intended for collaborative contributions. However, feedback and suggestions are welcome through the issues tab of the repository.


