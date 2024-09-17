# TimeCashier

## Description
This project is a web application built using Django and JavaScript.
It includes features such as user authentication, client management, and **time tracking based on user geolocation.**
The project uses various Django packages and libraries to enhance functionality and improve user experience.

## Features
- User authentication and authorization
- Client management
- Time tracking based on user geolocation
- Admin interface for managing data
- Email notifications

## Requirements
- Python 3.x
- Django 5.x
- Other dependencies listed in `requirements.txt`

## Development Setup
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
    ```
2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install development dependencies:
    ```sh
    pip install -r requirements/local.txt
    ```

4. Set up environment variables:
    ```sh
    cp .env.example .env
    ```
    Edit .env to include your environment-specific settings
5. Apply migrations and collect static files:
    ```sh
    python manage.py migrate
    python manage.py collectstatic
    ```
6. Run the development server:
    ```sh
    python manage.py runserver
    ```
7. Create a superuser to access the admin interface:
    ```sh
    python manage.py createsuperuser
    ```
8. Access the application at `http://localhost:8000`
9. Access the admin interface at `http://localhost:8000/admin`
10. Login with the superuser credentials created in step 7
11. Create clients and users to start tracking time.
