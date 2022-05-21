# Smart Park

Deployed on Heroku at https://smartpark-infinity.herokuapp.com/

## Tech Stack

**Client:** HTML, CSS

**Server:** Python, Django

**Database:** SQLite

## Run Locally

Clone the project

Clone the project

```bash
  git clone https://github.com/VOSID8/SmartPark.git
```

Go to the project directory

```bash
  cd smartpark
```

If you want use virtual environment

```bash
  virtualenv env
```

```bash
  env/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Add Security Key : Go to project's **settings.py** file and change the value of **SECURITY_KEY** variable to desired security key.

Run Migrations

```bash
 python manage.py makemigrations
```
```bash
 python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```
