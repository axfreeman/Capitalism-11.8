# Plan and checklist for Capitalism-11.6
Here is the plan for the installation. 
Can't promise to have followed it exactly
## Install
* pipenv shell
* pipenv install django
* pipenv install django-rest-framework
* pipenv install django-cors-headers
* pipenv install django-polymorphic
* pip install django-crispy-forms
## git
git bash in root directory
create gitignore in root directory
git add .
git commit -m"Initialise before project creation"
create github repo using VSCode
## Django setup
* django-admin startproject capitalism .
* py manage.py runserver to test.
* **Do NOT migrate (until user model has been created)**
* py manage.py startapp economy
* py manage.py startapp accounts
### settings.py
* add economy, accounts, rest_framework, polymorphic, corsheaders, crispy_forms, crispy_bootstrap4, to INSTALLED_APPS
* add these lines:
```
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
    CRISPY_TEMPLATE_PACK = "bootstrap4"
```
* add CORS lines
* add CORS to middleware above ``'django.middleware.common.CommonMiddleware'``,thus:
  * ``"corsheaders.middleware.CorsMiddleware",``
  * ``"django.middleware.common.CommonMiddleware",``
* STATICFILES
 ```STATICFILES_DIRS = [
        BASE_DIR / "static",
            "accounts/static/",
            "economy/static/"
        ]
```
* **NOTE do not put a forward slash at the start of these urls.**
* TEMPLATES
### urls.py
* in the root urls.py add ``path('api-auth/', include('rest_framework.urls'))``
### additional directories
* templates in root directory
* templates/accounts
* templates/economy
* templates/registration
  * ``https://docs.djangoproject.com/en/4.2/topics/settings/``
  * ``https://docs.djangoproject.com/en/4.2/ref/settings/``
* fixtures in root directory
* staticfiles in root directory
* static in root directory
* (root) static/css
* (root) static/js
* We want to avoid creating static files in the app folders because it adds an unnecessary layer of complexity
## copy relevant files into the root static folder
* w3.css
* w3 js files (I forget the name)
* font-awesome
* datatables.min.js
* all the json files to fixtures
## Configure urls 
* configure capitalism/urls.py with path('api-auth/', include('rest_framework.urls'))
* configure capitalism/urls.py to include accounts and economy
* create urls.py files in economy and accounts
## Create a custom user model
### Documentation 
[official](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/)
> You should also define a custom manager for your user model. If your user model defines username, email, is_staff, is_active, is_superuser, last_login, and date_joined fields the same as Django’s default user, you can install Django’s UserManager; however, if your user model defines different fields, you’ll need to define a custom manager that extends BaseUserManager providing two additional methods:...

[useful general guide](https://www.youtube.com/watch?v=RmRc8nDrAfs)\
[another guide](https://dev.to/earthcomfy/getting-started-custom-user-model-5hc)
* create custom user model
* modify settings with ``AUTH_USER_MODEL = 'accounts.User'``
* migrate
* create a superuser
* test
  
### Create login handling views
[The official method](https://docs.djangoproject.com/en/3.1/topics/auth/default/#all-authentication-views)

* copy login handling templates from Capitalism 10.5
* test creation and deletion of users

## Create and test a simulation model

Simulation objects are the fundamental entities through which users interact with the system. A simulation object is unique to a user (has a many-one relation to a user) and unique to a 'state' which is a field in the simulation object. It is in a one-many relation with a set of Commodities, Industries, SocialClasses, and Stocks which between them define a unique point in time that has been reached by an economy. The state can be one of the following:
* A 'Template' which defines the initial starting point of a simulation
* An 'Initial' state which is a deep copy of a Template and will be displayed in the user's interaction area
* Any one of a series of 'Successor' states which are created as the simulation evolves. 

Each successor state is a modified deep clone of the state from which it was generated

In any simulation except a Template or an Initial simulation, the State is in a one-one relation with its predecessor and, if it has a successor, that successor. Thus it is possible to traverse the trajectory of any simulation in some way to discover what happened at each point in time

There are a number of possible implementations of this concept eg foreign keys linking successive states. We will first try to implement it in this way but it could be implemented, for example, as a list in the User object.

###
* register Simulation with admin
* 