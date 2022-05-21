# Smart Park

Deployed on Heroku at https://smartpark-infinity.herokuapp.com/

Daily parking slots like Malls, private parkings etc as well as parking for events simply use ticket mechanism for cars getting parked. However, this method involves a lot of manforce which can be cut down upon as well as lacks security and efficient parking mechanism. We would be detecting number plates, storing them in our database on the arrival of the vehicle and its type and maintaining a record daily. On depart, document its departing time. Estimating how long the car is being parked and ensuring no vehicle is being parked for unusual hours. 

## Tech Stack

**Client:** HTML, CSS

**Server:** Python, Django, OpenCV, PyTorch

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
