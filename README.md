# Library project

Test project for innowise group company.
The application simulates the work of the library. 
There are two entities: the user and the book. 
The application allows you to view all users, 
display a list of their books, add new ones and 
edit books.

## Uses

django 2.2.3
postgres: database "library"

## Staring
```
$ git clone https://github.com/Nenu1985/library.git
$ cd library

$ python3 -m venv venv
$ venv\Scripts\activate (win)
$ source venv/bin/activate (linux)
$ python -m pip install -r requirements.txt


$ createdb library (postgres db, look at settings.py)

$ python manage.py migrate
$ python manage.py loaddata db.json
$ python manage.py test

$python manage.py runserver
```

# Useful info
## dump data
Write your current db data to json file:
```
python manage.py dumpdata -o db.json
```
## load data
````
python manage.py loaddata db.json
