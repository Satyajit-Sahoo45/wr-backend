# Backend Application Setup

## Clone the Repository:

"https://github.com/Satyajit-Sahoo45/ws-backend"

## Create a Virtual Environment::

### `python -m venv venv`

## Activate the Virtual Environment:

On windows:

### `venv\Scripts\activate`

On macOS/Linux:

### `source venv/bin/activate`

## Install Dependencies:

### `pip install -r requirements.txt`

## Add Database Url and Secret Key in .env file:

The DB_URL should be in this format:

### `postgresql://username:password@localhost:5432/testcaseDb`

## Initialize the Database:

### `flask db init`

### `flask db migrate`

### `flask db upgrade`

## Run the Application:

### python ./app.py
