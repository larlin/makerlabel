This project is to develop a webapplication that can directly print a label
for boxes, tools and other usefull uses for labels.

Dependecies:

    django-model-utils
    Lot's of latex packages:
        xcolor, array, inputenc, caption, adjustbox, wrapfig, geometry, isodate, parskip

Tweaks:
    
    Debian by default runs apache in a LANG=C enviroment.
    To fix this change the row with LANG=C /etc/apache2/envvars
    to LANG=en_US.UTF-8 or some other UTF-8 enviroment.

Start:
    Make sure dependecies are installed on the system.
    
    migrate django project:
        'python3 manage.py migrate'
    
    create super user for admin access:
        'python3 manage.py createsuperuser'
    
    start server:
        'python3 manage.py runserver'
    
    create a member in the database by going to 127.0.0.1:8000/admin/
    and logging in with the superuser created earlier.
