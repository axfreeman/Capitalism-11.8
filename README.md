# Purpose
This is the most complete version of the capitalism simulation using Django's Model Classes  
It is to be replaced by a Model-Free version.  
This is because Django's models are not polymorphic.  
That is to say, inheritance does not work properly.  
Attempted to correct this by usig django-polymorphic, but this proved too difficult and leads to obscurity.  
However this version does contain the basic structure and templating.
Therefore, it is a stepping-stone to a Model-free version.
It also serves as a test bed for the features that will eventually figure in the Model-free version
## Django setup
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
* We avoided creating static files in the app folders because it adds an unnecessary layer of complexity  
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
# User handing
Did not create custom user in the end. Additional complexity turns out to be unnecessary  
# Login handling views
[The official method](https://docs.djangoproject.com/en/3.1/topics/auth/default/#all-authentication-views)
Only the very basic, so that each user can have a dashboard and can create simulations from templates  
## Create and test a simulation model
Simulation objects are the fundamental entities through which users interact with the system.  
A simulation object is unique to a user (has a many-one relation to a user) and unique to a 'state' which is a field in the simulation object.  
It is in a one-many relation with a set of Commodities, Industries, SocialClasses, and Stocks which between them define a unique point in time that has been reached by an economy.  
The state can be one of the following:
* A 'Template' which defines the initial starting point of a simulation
* An 'Initial' state which is a deep copy of a Template and will be displayed in the user's interaction area
* Any one of a series of 'Successor' states which are created as the simulation evolves. 

Each successor state is a modified deep clone of the state from which it was generated  

In any simulation except a Template or an Initial simulation, the State is in a one-one relation with its predecessor and, if it has a successor, that successor. Thus it is possible to traverse the trajectory of any simulation in some way to discover what happened at each point in time  

There are a number of possible implementations of this concept eg foreign keys linking successive states. We will first try to implement it in this way but it could be implemented, for example, as a list in the User object.

