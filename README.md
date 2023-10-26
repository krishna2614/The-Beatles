# The Beatles

### To run the code follow the provided steps:

- Prerequisites:
  - Python
  - Database to save .sql file (I have used PostgreSQL)

1. Create Virtual Environment
    - python -m venv venv
2. Activate the virtual environment
    - For Windows: .\venv\Scripts\activate
    - For Mac: source ./venv/bin/activate
3. Install required libraries
    - pip install -r requirements.txt
4. Migrate the database
    - python manage.py makemigrations
    - python manage.py migrate
5. Run the server
    - python manage.py runserver
