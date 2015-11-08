BlueButton on FHIR Developer Account
====================================

This is the Developer Account Framework for
BlueButton on FHIR.
 
This framework has been developed using Python 3.4 and Django 1.8. 

This version implements a Custom User model that uses email as username.
Django-registration-redux is also implemented to issue email to complete 
registration. This required some overrides to use email and not username.

The custom user model is in accounts.

The custom user model also implements multi-factor authentication. 
This uses telephone and carrier information in the User model to send
a 4-digit code to the cell phone of the user as part of the login process.

The SMS routines require the user to pick a carrier identity. The app then
uses email/smtp to send a 4-digit code to the user. This takes advantage of
most (all) carriers having an email to SMS gateway.

The phone number format in the usermodel needs some refinement to allow 
relaxed number formatting. eg. allowing more than +12025551234 as an
 input format.

On Mac OS X you need to have xcode command line tools installed.
Install Using the following command: 
xcode-select --install

Setup:

1. Configure local.ini
2. run pip install -r bofhirdev/config/requirements.txt
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage,py createsuperuser
6. python manage.py runserver
7. login to localhost:8000/admin and configure sites
8. set SITES_ID in settings.py to match key of record in admin/sites
