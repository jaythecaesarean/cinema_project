# Cinema Project

## Installation

Clone the repository:
```bash
git clone https://github.com/jaythecaesarean/cinema_project.git
```
Then, go to the clone repo / directory 

```python
cd <path/to/the/cloned/repo>
```

It is recommended to use virtualenv or virtualenv-wrapper for the project. You may check [virtualenv-wrapper here](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Then activate it after installation.
Make sure that your are using Python3 (3.7+)

On your newly-cloned repo, intall the dependencies:
```bash
pip3 install -r requirements.py
```

## Setup
Note: This a prototype project which uses sqlite3 as its database. You may want to change it.
First you need to prepare the database and create migratons:
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a new superuser (you may skip this step).
```bash
python manage.py createsuperuser
```
It will then prompt for username, email, and password.

You may now run a local development server:
```bash
python manage.py runserver
```

## Fetching data
The data are fetched from the json files then save to the database.
On you browser or any API client, please go (GET request for API Clients) to these three URIs
```bash
http://127.0.0.1:8000/fetch/coming_soon
http://127.0.0.1:8000/fetch/schedules
http://127.0.0.1:8000/fetch/now_showing
```
These will initialize the data in your database. The expected response for the requests is SUCCESS 200 (OK) status code.
Note: Change <http://127.0.0.1:8000> to the correct hostname and port if you run the server differently.


## Retrieving Data
Use GET for all of the request below.

To get all the list of movies:
```bash
http://127.0.0.1:8000/movies
```

To get all the movie schedules:
```bash
http://127.0.0.1:8000/movies/<uuid.of.the.movie>/schedules 
```


