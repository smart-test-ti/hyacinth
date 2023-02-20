pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations hysite
python manage.py migrate hysite