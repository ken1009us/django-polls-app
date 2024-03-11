# Django Polls Application

This is a polls app. The goal is to practice Django.

## Setup

1. create a virtual environment

```bash
$ python -m venv venv
```

2. Activate the virtual environment

```bash
$ source venv/bin/activate
```

3. Install Django

```bash
python -m pip install Django
```

4. Set up a database (if necessary)

5. Create a project

Python package for the project.

```bash
$ django-admin startproject mysite
```

6. Test the development server

```bash
python manage.py runserver
```

7. Create the app

The apps can live anywhere on the Python path. I'll create the poll app in the same directory as my manage.py file so that it can be imported as its own top-level module, rather than a submodule of mysite.

```bash
python manage.py startapp polls
```

## Write the first view

1. Open the polls/views.py

```py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

To call the view, we need to map it to a URL - and for this we need a URLconf.

2. Create a urls.py file in the polls dir

3. In the polls/urls.py, we want map the view to a URL

```py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

4. Point the root URLconf at the polls.urls module.

In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list.

```py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

## Database setup

1. Setup the Database

By default, the configuration uses SQLite so I use SQLite.

Go to settings.py to change the database if you want.

Use the command line below to create any necessary database tables according to the database settings in the mysite/settings.py file and the database migrations.

```bash
$ python manage.py migrate
```

Use the command below to view the database.

```bash
$ sqlite3  db.sqlite3
```

```bash
sqlite> .tables
```

2. Define the data models

- Question
 - A Question model has a question and a publication date

- Choice
 - the text of the choice and a vote tally. Each Choice is associated with a Question

In the models.py file

```py
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

```

