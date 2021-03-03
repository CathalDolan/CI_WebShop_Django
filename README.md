python3 manage.py runserver
Items inside [square brackets] should be named according to the project being worked upon

# 1. Initial Set-up and Creating a Django Project

1. Install Django using PIP (Pip Installs Packages). In console window type 
    - pip3 install django
2. Create Project. In console window type:
    - django-admin startproject [project_name] . (Full stop to put into current directory)
3. Create a .gitignore file:
    - touch .gitignore
    - *.sqlite3
    - *.pyc 
    - __pycache__
4. Run initial migration. In console window type python3 manage.py migrate
5. Create a SuperUser to access admin:
    - In console window type python3 manage.py createsuperuser
    - Add username
    - Add email address
    - Add password (Min 8 characters)
    - Confirm password

# 2. Authentication
## 2.1 Set-Up
1. Install Djano Allauth package:
    - pip3 install django-allauth
2. Extract settings from <https://django-allauth.readthedocs.io/en/latest/installation.html>
    - Check if "'django.template.context_processors.request'" is included in settings.py "TEMPLATES". If not, add it.
    - Copy "AUTHENTICATION_BACKENDS" from sqlite3
    - Paste immediately beneath TEMPLATES in settings.py
    - Remove the 3 dots top and bottom
    - Copy from "INSTALLED_APPS":
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
    - Paste into "INSTALLED_APPS" in settings.py
    - Beneath "AUTHENTICATION_BACKENDS" in settings.py add:
        SITE_ID = 1
    - Go to urls.py
        - In "urlpatterns" add a path to "allauth":
            path('accounts/', include('allauth.urls')) - There may be an automatic way to do this
        - Add "include" to django.urls imports
3. Update the database with new app by migrating: (ensure all changes have been saved)
    python3 manage.py migrate
4. Create template folders for allauth:
    mkdir templates
    mkdir templates/allauth

## 2.2 Update default domain name in admin (Required for SM connection)
    - Expose site: python3 manage.py runserver
    - Go to admin section by adding "/admin" to url
    - Login
        - CathalD
        - Navan1976
    - In "Django Administration" navigate to "SITES" and click on "Sites"
    - Click on "example.com"
        - Update "Domain name" to [domain_name].example.com
        - Update "Display name" to project name. Can use capitals and spaces
        - Click "Save"

## 2.3 Email Set-Up (I think!)
    - Go to settings.py
        - Beneath SITE_ID add: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        - Beneath that add: (All can be found in <https://django-allauth.readthedocs.io/en/latest/configuration.html>)
            ACCOUNT_AUTHENTICATION_METHOD = 'username_email' (Tells allauth we want to use usernames or emails for Authentication)
            ACCOUNT_EMAIL_REQUIRED = True (EMail is required to register)
            ACCOUNT_EMAIL_VERIFICATION = 'mandatory' (Email must be authenticated to register)
            ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True (User must add email twice when registering)
            ACCOUNT_USERNAME_MIN_LENGTH = 4 (Username must be a minim of 4 characters)
            LOGIN_URL = 'accounts/login/' (Login url)
            LOGIN_REDIRECT = '/' (Where user goes after logging in)
    - Freeze the requirements:
        pip3 freeze > requirements.txt

## 2.4 Copy allauth templates
    This allows us to customise the pages created by default by allauth. In the cli:
        cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./CI_WebShop_Django/templates/allauth
    - Removed any unrequired templates such as openid or tests
    - If not present, add a base.html file to the allauth folder
    - Add "allauth" to the project templates. The root templates are also created at this point (this can also be done later, see 4.3.5). 
        - Go to project settings.py
        - Within "DIRS" in "TEMPLATES" add two paths:
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth') 

# 3 Set-up Project Base HTML

1. Create a "base.html" file in the project folder
2. Go to <https://getbootstrap.com/docs/4.6/getting-started/introduction/>
    **Note**: Bootstrap 4 is employed as opposed to Bootstrap 5, because
    some changes in the latter made the tutorial code unworkable.
3. Navigate to "Starter Template" and copy complete
4. Paste it into project base.html
5. Make sure both Popper.js and Bootstrap JS are included and in this order (or combined)
6. If jQuery script is absent, navigate to <https://code.jquery.com/>
7. From jQuery Core, select most up todate stable "slim" by clicking on it and copying the
8. Paste it above the popper.ja or combined script
9. Add backwards compatibility to browsers via metat tags. Add:
    <meta htt-equiv="X-UA-Compatible" content="ie=edge">
10. Cut script lines from the bottom and paste them beneath Bootstrap link and above "title" tags
11. Add {% load static %} to the very top of the page
12. Wrap the header elements in blocks for later reuse.
    - {% block meta %}
    - {% block corecss %}
    - {% block corejs %}
13. Beneath each header block insert additional blocks to allow for addition of extras on later pages
    - {% block extrameta %}
    - {% block extracss %}
    - {% block extrajs %}
14. Add blocks and extra blocks within the body (All positioned beneath "header" tags)
    - Title: <title>[title]{% block extr_title %}{% endblock %}</title>
    - Page Header: {% blockpage_header %}
    - Block Content: {% block content %}
    - Extra JS: {% block postloadjs %}
15. All blocks to include {% endblock %}


# 4 Setup an App (Home in this example)

## 4.1 Basic Creation
1. Create the basic app:
    python3 manage.py startapp [home]
2. Create a templates directory within the new app:
    mkdir -p [home]/templates/[home]
3. Add the app name to App settings.py
    - Open App settings.py
    - Go to "INSTALLED_APPS" section
    - Add the new app name to the bottom of the list
        - Encase in single strokes and put a comma at the end: e.g. 'home',

## 4.2 Create basic html page
1. Create [home/index].html file within inner app "[home]" folder
2. In new file, add extend and load blocks at the top of the page
    - {% extends "base.html" %}
    - {% load static %}
    - {% block content %}

## 4.3 Create a View to render html template 
1. Navigate to the App views.py
2. Define a view (In this example for home/index)
    def [index](request):
        return render(request, '[home/index.html]')
3. Create an App urls.py file
    - Add the imports
        from django.contrib import admin
        from django.urls import path
    - Create an empty path to indicate that this is the route URL and it's going to render views.index with the name of home
        urlpatterns = [
            path('', views.index, name='home'),
        ]
    - Import "views" from the current directory:
        from . import views
4. Add a path in the Project urls.py
    - Go to project urls.py
    - in "urlpatterns" beneath existing paths add:
        path('', include('home.urls')),
        path('products/', include('products.urls')),
5. Add App to project settings and wire up template directories
    - Go to project settings.py
    - Under "INSTALLED_APPS" add '[home]'
    - 2.4 "Copy allauth templates" can also be done here

## 4.4 Connecting to database

If the app takes advantage of a database, additional actions are required.

1. In the App folder, create a new folder called "fixtures"
2. If there are existing Json fixture files, add them
3. We need to create some "models" for the fixtures to go into:
    - Go to App models.py
    - Create class(es)
4. Make migrations:
    - Do a dry run first
        python3 manage.py makemigrations --dry-run
    - If necessary, install "pillow"
        pip3 install pillow
    - To make actual migrations
        python3 manage.py makemigrations
    - Run migrate with plan first to be sure all is OK
        python3 manage.py migrate --plan
    - If yes, run migrate
        python3 manage.py migrate
    - **Note**: It's best to specify which App the migrations are being done from. Above migrates all
5. Register the model in App admin.py
    - Go to App admin.py file
    - Import the relevant mnodel
        from .models import [model_name]
    - Register it. This goes at the end of the page
        admin.site.register([model_name])

6. Load the fixtures data
    python3 manage.py loaddata [fixture_jsonFile_name]

## 4.5 Tidying the Database Admin

Rewatch Products Set-up, Products Admin, 2nd Video in tutorials

# 5 Setup Media & Static folders
1. In project folder create a new sub-folder called "media"
2. In project folder create a new sub-folder called "static"
3. Within the static folder create another sub-folder called "css"
4. Within the css folder, create a file base.css
5. Add css link in base.html
    - Within the "corecss" blocks and just before "endblock" add:
        <link rel="stylesheet" href="{% static 'css/base.css' %}">
6. Link up the "static" file:
    - Go to settings.py
    - Scroll to "STATIC_URL"
    - Immediately beneath add the tuple:
        STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    - **Note:** No "static route" added as it interferes with Amazon Web Services
7. Link up the "media" file:
    - Add a line space beneath "STATICFILES_DIRS" and add:
        MEDIA_URL = '/media/'
    - Immediately beneath that add:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
8. Allow Djnago to see the "media" files:
    - Go to project urls.py and add to import the settings:
        from django.conf import settings
    -  Immediately beneath that, import the static function:
        from django.conf.urls.static import static
    - Use the static function to add "media" to our list of URL's:
        - In "urlpatterns", on the same line as the closing square bracket add:
            + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 6 Setup Fonts & Icons
Fonts based on Google Fonts and icons from Font Awesome
## 6.1 Fonts
    1. Navigate to fonts.google.com
    2. Search for required font and open it
    3. On right side of the screen, copy the"<link>" code
    4. Go to "base.html" file and paste the link(s) in immediately beneath the Bootstrap link inside the "corecss" blocks
## 6.2 Icons
There is an option to create aFontawesome account. In this instance we'll use a cdn 
    1. Go to https://www.codegrepper.com/code-examples/whatever/font+awesome+cdn
    2. Copy the latest or your preferred link
    3. Insert it immediately beneath the fonts link within the "corecss" blocks


# 7 Manipulate the Database from CLI using Shell - Update Products enmasse
This allows us to change the database from the terminal window. It is configured to our settings.py file
so can act just like us writing code in a view.
1. Open Shell
    python3 manage.py shell
2. Import area to be edited
    from [app_name].models impor [App_name]
3. Create a variable for items not to be included
    [var_name] = ['category', 'category_too']
4. Exclude the items in the var
    [var_name_too] = [App_name].objects.exclude(category__name__in=[var_name])
5. Run a for loop to find all products to be updated
    for x in [var_name_too]
        x.has_sizes = True
        x.save()
        Hit return key again
6. Run a count 
    [Var_name].objects.filter([db_filed_name]=True).count()
7. Exit shell   exit()
