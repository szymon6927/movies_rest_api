# Movies REST API

Netguru recruitment task

Application URL [http://movies-netguru.szymonmiks.pl](http://movies-netguru.szymonmiks.pl)

## Getting Started
To start the project locally

Clone repository
```
$ git clone https://github.com/szymon6927/movies_rest_api.git
```

I recommend using  `virtualenv`
```
$ virtualenv venv

for unix users:
$ source venv/bin/activate 

for windows users:
$ source venv/Scripts/activate
```

then 
```
$ cd movies_rest_api
```

copy .example.env and create .env set `DEBUG=True` and `SQLITE=True`
you have to set also `OMDb_API_KEY` and `SECRET_KEY`

next step is to install all required packages
```
$ pip install -r requirements.txt
```

before running app, make all needed migrations
```
$ python manage.py migrate
```

now you can start
```
$ python manage.py runserver
```

open a browser and go to
```
http://127.0.0.1:8000
```

### Prerequisites

To start you have to have installed `Python 3.7.2`


## Running the tests

To run the tests in project directory type
```
$ make
```

If you don't have `Make` at your computer type

```
$ python manage.py test
```


## Deployment

To deploy changes all you need to do is to push changes into
`master` branch. I used [Buddy](https://buddy.works/) CI/CD tools.


## Authors

* **Szymon Miks** - [website](https://szymonmiks.pl/)

