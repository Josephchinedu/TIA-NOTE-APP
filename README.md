<div id="top"></div>
<br />
<div align="center">
    <a href="https://github.com/libertytechx">
        <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
    <h3 align="center">Tunga TIA DIARY NOTE</h3>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#built-with">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing or running the application locally</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About The Project
This is a simple diary note application that allows users to create, read, update and delete their diary notes.<br />It also allows users to set reminders for their diary notes. <br />Users can also have their notes save in csv or pdf.<br />The application is built with Django and Celery.
<br />

## Usage
Postman was used to test the API endpoints. <br />
Collection: https://documenter.getpostman.com/view/11580677/2s9YR6ZDeG
<br />

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Create and activate virtualenv for this project.
```bash
python -m venv venv
```
```bash
# for windows 
venv\scripts\activate

# for mac 
venv/bin/activate
```
4. Install dependencies.
```bash
pip install -r requirements.txt
```
5. create .env file and add the content of .env.example to it
6. Database used is postgresql
7. make migrations and migrate
```bash
python manage.py makemigrations account main
```
8. migrate
```bash
python manage.py migrate
```
9. install redis and run redis server. 
```bash
# for windows
 https://github.com/microsoftarchive/redis/releases

# for mac
brew install redis

# run redis server
# on windows
# locate redis-server.exe in the redis folder located in the C drive, probably C:\Program Files\Redis
# run redis-server.exe

# on mac
redis-server
```
10. create superuser
```bash
python manage.py createsuperuser
```
11. create note categories
```bash
python manage.py add_categories

# to modify or add more categories, edit the main/management/commands/add_categories.py file
```
12. create periodic tasks
```bash
python manage.py create_periodic_tasks

# to modify or add more periodic tasks, edit the main/management/commands/create_periodic_tasks.py file
```
13. run celery worker
```bash
celery -A core.celery worker --loglevel=INFO --concurrency 1 -P solo
```
14. run celery beat
```bash
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
15. run the application
```bash
python manage.py runserver
```
16. run tests
```bash
pytest
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<p align="right">(<a href="#top">back to top</a>)</p>