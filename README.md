# MultiTools
A collection of django-based apps


This Project requires, at least, a Python virtual environment to run the Django project. 

ADD A VIRTUAL ENVIRONMENT (COMMAND LINE) (WARNING: May have issue with script permission depending on your OS setup):
To add virtual environment through command line, execute the following commands:

pip install virtualenv
virtualenv -p python3 venv
cd venv/Scripts
./Activate.ps1

pip install django
pip install python_gitlab


ADD VIRTUAL ENVIRONMENT (VISUAL STUDIO 2022):
To add virtual environment using Visual Studio 2022, do the following:

- In the Solution Explorer, right click on "Python Environments", then select "Add Environment"
- The "Add Environment" window pops-up. Change the "Name" field to your desired virtual environment name.
- Press "Create" button and wait for the process to finish installing the required environment.

NOTE: when cloning this repository for the first time, please remove an existing virtual environment and create a new one.


HOW TO ADD AN APP TO THE PROJECT:
To add an app to the project, follow these steps:

1. add a folder with the name of your app to the root folder of the repository.
2. add the view script (.py) inside the folder of your app. Ideally, the view script has the name of the folder and ends with "View"
3. In your view script, add a function to display the home page of your app. (Here is a good reference for creating view scripts: https://www.geeksforgeeks.org/views-in-django-python/)
4. in the WebAppCollection folder, you can find the script "settings.py".
5. In the settings.py script, look for the variable array "INSTALLED_APPS".
6. Add the name of the folder that you have added in step 1 to the variable array "INSTALLED_APPS" (ideally, near the top of the array).
7. Open the script "urls.py" and import the function that you have made in step 3.
8. look for the variable array "urlpatterns" then add the base URL of your app to the variable array "urlpatterns" (ideally, same base url with the name of the app folder... And don't forget to import the new app's view.)


HOW TO RESET SQLITE3 DATABASE BASED ON THE MODELS.PY:
python manage.py migrate <app_name> zero 
python manage.py makemigrations <app_name>
python manage.py migrate <app_name>


HOW TO ADD A SUPERUSER FOR THE DJANGO ADMIN:
py manage.py createsuperuser


HOW TO ADD STATIC FILES (.JS, .CSS, IMAGES, ETC) TO PROJECT
python manage.py collectstatic


HOW TO RUN UNIT TESTS (REQUIRES COVERAGE LIBRARY):
coverage run manage.py test -v 3

============================================== DATABASES ==============================================================
Log Search:
auth_user --┐
			├> server_users
servers	----┤
			├> server_services
services ---┤
			├> service_logfiles
logFiles ---┘


Externalizer:
servers --------┐
                ├> env_server
environments ---┼-----------------------┐
				├> env_property         ├> env_service_property
properties -----┤                       |
				├> service_property ----┘
services -------┘

PROPERTY VALUE PRIORITY: env_service_property -> env_property -> service_property

CREDENTIALS PRIORITY: server_users -> server


MINIMUM DATA REQUIREMENTS:
Configurations - data used for commands execution
UsersDetails - Gitlab data
LogFiles - Data on types of logfiles
Environments - Environment data
Servers - Server data including IPs and credentials
EnvServers - Data on server category per environment


IMPORT ERROR FIX (DJANGO ADMIN):
Edit the import_export resources.py, usually located at:

	<python_library>/Lib/site-packages/import_export/resources.py

Replace the line in __init__ method of the resource class:

	self._meta.import_id_fields = xxxx

with the follow block of code:

	for key, value in self.fields.items():
		if 'ID' in key:
			self._meta.import_id_fields = [key]
            break
