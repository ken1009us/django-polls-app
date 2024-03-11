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

```shell
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

## Introducing the Django Admin

1. Creating an admin user

```bash
$ python manage.py createsuperuser
```

Go to http://127.0.0.1:8000/admin to see the admin UI. Now, we need to make the poll app modifiable in the admin.

In the polls/admin.py file:

```py
from .models import Question

admin.site.register(Question)
```

## Writing more views

1. Add more views for polls app

In the `views.py` file

```py
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

In the `urls.py` file

```py
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

2. Write views that actually do something

Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

In the views.py file:

```py
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```

There’s a problem here, though: the page’s design is hard-coded in the view.

Create a directory called `templates` in the `polls` directory. Django will look for templates in there.

Within the `templates` directory we have just created, create another directory called `polls`, and within that create a file called `index.html`.

```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

update `views.py` file:

```py
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

3. Raising a 404 error

Now, if we cannot find the question ID stored in the DB, we should return HTTP status error code to the user.

```py
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist as exc:
        raise Http404("Question does not exist") from exc

    template = loader.get_template("polls/detail.html")
    context = {"question": question}

    return HttpResponse(template.render(context, request))
```

Add `polls/detail.html`

```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

4. Removing hardcoded URLs in templates

- The problem with this hardcoded, tightly-coupled approach is that it becomes challenging to change URLs on projects with a lot of templates

```html
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

change to:

```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

so that we can change the URL of the polls detail view to something else


5. Namespacing URL names

How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

- add an app_name to set the application namespace in `urls.py` file

```py
app_name = "polls"
```

Now change the `polls/index.html` template from:

```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

to point at the namespaced detail view:

```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

## Write a minimal form

1. Update the detail template to be the form

In the `polls/detail.html`:

```html
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>
```

The above template displays a radio button for each question choice.

2. Create a vote function

In the views.py file

```py
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```
- `F("votes") + 1` instructs the database to increase the vote count by 1

- After incrementing the choice count, the code returns an `HttpResponseRedirect` rather than a normal HttpResponse. `HttpResponseRedirect` takes a single argument: the URL to which the user will be redirected

- As the Python comment above points out, you should always return an `HttpResponseRedirect` after successfully dealing with `POST` data. This tip isn’t specific to Django; it’s good web development practice in general

- We are using the `reverse()` function in the `HttpResponseRedirect` constructor in this example. This function helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view.

3. Add the results template

```html
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

## Use generic views: Less code is better

The detail() and results() views are very short – and, as mentioned above, redundant. The index() view, which displays a list of polls, is similar. \

These views represent a common case of basic web development: getting data from the database according to a parameter passed in the URL, loading a template and returning the rendered template. Because this is so common, Django provides a shortcut, called the “generic views” system. \

Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app. For example, the ListView and DetailView generic views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object” respectively. \

1. Amend URLconf

```py
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

Note that the name of the matched pattern in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".

2. Amend views

```py
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-publish_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
```

Each generic view needs to know what model it will be acting upon. This is provided using either the model attribute (in this example, model = Question for DetailView and ResultsView) or by defining the `get_queryset()` method (as shown in IndexView). \

By default, the `DetailView` generic view uses a template called <app name>/<model name>_detail.html. In our case, it would use the template "polls/question_detail.html". The `template_name` attribute is used to tell Django to use a specific template name instead of the autogenerated default template name. We also specify the `template_name` for the results list view – this ensures that the results view and the detail view have a different appearance when rendered, even though they’re both a DetailView behind the scenes. \

Similarly, the `ListView` generic view uses a default template called <app name>/<model name>_list.html; we use `template_name` to tell `ListView` to use our existing "polls/index.html" template. \

In previous parts of the tutorial, the templates have been provided with a context that contains the question and `latest_question_list` context variables. For `DetailView` the question variable is provided automatically – since we’re using a Django model (Question), Django is able to determine an appropriate name for the context variable. However, for `ListView`, the automatically generated context variable is `question_list`. To override this we provide the `context_object_name` attribute, specifying that we want to use `latest_question_list` instead. As an alternative approach, you could change your templates to match the new default context variables – but it’s a lot easier to tell Django to use the variable you want. \

