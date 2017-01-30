# How to install

First, set the following environent variables:
* SURVEY_SECRET: the secret key for the application. Use a random number: `>>> import binascii; binascii.hexlify(os.urandom(24))`
* DATABASE_URL: [sqlalchemy database uri](http://docs.sqlalchemy.org/en/latest/core/engines.html). You might need to install additional python packages if you do not use sqlite
* EMAIL_USERNAME: gmail username to be used for sending emails with results. If you do not specify this variable, the "send" page will show the csv instead of sending to users
* EMAIL_PASSWORD: gmail password


After setting theses variables, clone this repository and install the requirements:

```bash
$ git clone https://github.com/JoaoFelipe/prov-survey.git
$ pip install -r prov-survey/requirements.txt
```

Go to the folder and initialize the database:
```bash
$ cd prov-survey
$ python manage.py db init
```

Configure the database in the *migrations* folder and migrate the database:
```bash
$ python manage.py db migrate
$ python manage.py db upgrade
```

Compile translations
```bash
$ cd surveys
$ pybabel compile -d translations
```

Start the server:
```bash
$ flask --app=surveys
```

# Extra

## Reset database

```bash
$ python manage.py db downgrade base
$ python manage.py db upgrade
```

## Translation

[Flask-Babel documentation](https://pythonhosted.org/Flask-Babel/)

Extract text from source:
```bash
$ cd surveys
$ pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

Create new translation
```bash
$ pybabel init -i messages.pot -d translations -l <lang>
```

Update existing translations
```bash
$ pybabel update -i messages.pot -d translations
```

Compile translations
```bash
$ pybabel compile -d translations
```
