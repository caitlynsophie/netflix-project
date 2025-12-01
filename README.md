### Deployment

After activating the virtual environment, do the following steps:

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py load_data`
4. `python manage.py runserver`