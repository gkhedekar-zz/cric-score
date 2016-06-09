Our Cricket App !

How to run the API on your localhost:
1. install flask, gunicorn and sqlalchemy libraries on your laptop or virtual environment 
(personally i use virtualenv since it does not mess up with the default python installation on your computer.)

To install virtualenv
sudo pip install virtualenv

create a project dir:
---->> mkdir ~/cricket_scorer
---->> cd ~/cricket_scorer

create virtualenv
---->> virtualenv cricket_scorer

start virtualenv
---->> source cricket_scorer/bin/activate

install gunicorn and flask
---->> pip install gunicorn flask

install sqlalchemy (orm to handle database)
---->> pip install SQLAlchemy

2. Create the git dir and pull the project

3. Start flask/gunicorn server to serve requests
---->> python app.py

4. Access the page at http://127.0.0.1:5000/
