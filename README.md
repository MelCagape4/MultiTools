# MultiTools
A collection of django-based apps

This Project requires, at least, a Python virtual environment to run the Django project. 


DEPLOYMENT PROCEDURES:
A) Clone Repository
B) Open Visual Studio Project (WebAppCollections.sln)
C) Add Environment:
	1) In the Visual Studio toolbars, click on the "virtualenv" dropdown box.
 	2) Select "Add Environment..." menu item.
  	3) Fill-in the following:
  	   - Name = folder name of the virtual environment which resides on the repository folder.
  	   - Install packages from file = The value should be the path to "requirements.txt" file.
  	   - Set as current environment = Check this box to set as default environment.
  	4) Click "Create" button to create the environment and download the necessary packages.
D) Open a Powershell and go to the repository folder (/MultiTools).
E) Go to the "Scripts" sub-folder located inside the environment folder that has been created in Visual Studio (/MultiTools/<environment-name>/Scripts):
F) Activate the virtual environment by running the following commands:

./Activate.ps1
cd ../..

G) Execute the following commands in sequence:

python manage.py makemigrations logsearch
python manage.py makemigrations externalizer
python manage.py makemigrations	dataporter
python manage.py migrate logsearch
python manage.py migrate externalizer
python manage.py migrate dataporter
python manage.py migrate
python manage.py collectstatic

H) Create Superuser:

python manage.py createsuperuser

I) Run the Django Server:

python manage.py runserver

J) Log into Django Admin page using the useruser that has been created: http://127.0.0.1:8000/toolsadmin/login/?next=/toolsadmin/

K) Update the import_export package's resources.py located in the virtual environment (MultiTools/<environment-name>/Lib/site-packages/import_export/resources.py):
	1) Add the code below in the Resource class's __init__ method, just below the line "self.fields = deepcopy(self.fields)"
	
        for key, value in self.fields.items():
            if 'ID' in key:
                print(key)
                self._meta.import_id_fields = [key]
                break


L) Populate the database using imports from SCV files (IMPORT the files below in sequence):
SysConfig-xx.csv = Configurations
LogFile-xx.csv = LogFiles
Environment-xx.csv = Environments
Server-xx.csv = Servers
EnvServer-xx.csv = EnvServers


M) Add "UsersDetails" data for dataporter:
	1) Create a Personal Access Token to be used to access the repositories.
	2) Fill-in the data of the UsersDetails:
		RepositoryURL - The base URL of the repositories. (E.G. https://github.com)
		RepositoryPrivateToken - The Personal Access Token created to access the repositories


N) Add "Server users" Credentials for dataporter (services access) and Log Search Apps:
	1) Fill-in the user credentials per server.


O) Fill-in "Server" credentials per server to be used as a default credential when no credential is found in "Server users".

APPS URLs:
DATAPORTER: http://127.0.0.1:8000/dataporter/
EXTERNALIZER: http://127.0.0.1:8000/externalizer/
LOGSEARCH: http://127.0.0.1:8000/logsearch/


=====================================================================================================================================

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
