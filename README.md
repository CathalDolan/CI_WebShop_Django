python3 manage.py runserver

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

# 3 Set-up Base HTML's

1. Create a "base.html" file in the project folder
2. Go to <https://getbootstrap.com/docs/5.0/getting-started/introduction/>
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
    - {% block corfecss %}
    - {% block corejs %}
13. Beneath each header block insert additional blocks to allow for addition of extras on later pages
    - {% block extrameta %}
    - {% block extracss %}
    - {% block extrajs %}
14. Add an extra title block inside the title
    - <title>[title]{% block extr_title %}{% endblock %}</title>