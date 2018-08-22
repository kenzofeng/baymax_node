pip install -r requirements.txt
nohup python manage.py runserver 0.0.0.0:51234 > /usr/locallogs/baymax.log 2>&1 &