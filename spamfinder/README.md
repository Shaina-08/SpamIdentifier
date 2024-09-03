Django Spam Management System


This Django project is a Spam Management System that allows users to sign up, log in, add phone numbers to a spam list, view spammers, and search for spam numbers. It uses Django’s built-in authentication system and REST framework for API interactions.


User Signup: Users can sign up and log in.
Add Spam: Authenticated users can add phone numbers to the spam list.
View Spammers: Users can view a list of reported spammers.
Search: Users can search for spam numbers by phone number or name through an API.
API Authentication: JWT tokens are used for secure API access.

Setup
Prerequisites

Python 3.12 or higher
Django 5.x or higher
Django REST framework
django-rest-framework-simplejwt
PostgreSQL or db.sqlite3

Installation

Install Dependencies

Create a virtual environment and install the required packages.

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Setup the Database

Update the DATABASES setting in settings.py if using PostgreSQL or any other database.

Run Migrations


python manage.py migrate
Create a Superuser

python manage.py createsuperuser
Run the Development Server


python manage.py runserver
API Endpoints

Signup

URL: /signup/
Method: POST
Parameters:
phone_number (string): The phone number of the user.
password1 (string): The password for the user.
password2 (string): Confirmation of the password.
email (string): The email address of the user.
name (string): The name of the user.
Response:
Success: Redirects to the add_spam page.
Error: Returns form errors and a 400 status code.

Login
URL: /login/
Method: POST
Parameters:
phone_number (string): The phone number of the user.
password (string): The password for the user.
Response:
Success: Redirects to the add_spam page and returns JWT tokens.
Error: Returns a message and 400 status code.


Add Spam
URL: /add_spam/
Method: POST
Headers:
Authorization: Bearer <access_token>
Parameters:
phone_number (string): The phone number to be added to the spam list.
Response:
Success: Returns a message and 201 status code.
Error: Returns an error message and appropriate status code.


View Spammers
URL: /view_spammers/
Method: GET
Headers:
Authorization: Bearer <access_token>
Response:
Success: Returns a JSON list of spammers with their phone numbers, names, and emails.
Error: Returns an error message and 401 status code if not authenticated.


API Login
URL: /api_login/
Method: POST
Headers:
Content-Type: application/json
Payload:
json
 code
{
    "phone_number": "string",
    "password": "string"
}
Response:
Success: Returns JWT tokens.
Error: Returns an error message and 400 status code.


Search
URL: /search/
Method: GET
Parameters:
query (string): The query to search for.
type (string): The type of search (phone or name).
Response:
Success: Returns a JSON list of search results.
Error: Returns an error message and 400 status code for invalid parameters.


Testing
To run the tests, use the following command:

pytest
