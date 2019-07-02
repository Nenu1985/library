# Library project

Test project for innowise group

## Uses

django 2.2.3
postgres: database "library"

## Staring
```sh
$ git clone https://github.com/Nenu1985/library.git
$ cd library

$ python3 -m venv venv
$ pip install -r requirements.txt

$ createdb library

$ python manage.py migrate
$ python manage.py collectstatic
```

