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

In the `models.py` file

```py
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

```

The model code gives Django a lot of information. With it, Django is able to:

- Create a database schema (CREATE TABLE statements) for this app.
- Create a Python database-access API for accessing Question and Choice objects.

3. Activate the models

To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting.

- Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation.

In the settings.py file

```py
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

```bash
$ python manage.py makemigrations polls
```

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

```bash
$ python manage.py sqlmigrate polls 0001
```

The sqlmigrate command takes migration names and returns their SQL. The sqlmigrate command doesn’t actually run the migration on your database

Run migrate again to create those model tables in your database:

```bash
$ python manage.py migrate
```

4. Use __str__() methods to return the helpful message

```py
def __str__(self):
    return self.question_text
```

5. Use `python manage.py shell` to manipulate the free API.

```bash
>>> from polls.models import Choice, Question

>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>

>>> Question.objects.filter(question_text__startswith="What")
<QuerySet [<Question: What's up?>]>

>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

>>> q = Question.objects.get(pk=1)

>>> q.choice_set.all()
<QuerySet []>

>>> q.choice_set.create(choice_text="Not much", votes=0)
>>> q.choice_set.create(choice_text="The sky", votes=0)
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

>>> c.question
<Question: What's up?>

>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

>>> c.delete()
```