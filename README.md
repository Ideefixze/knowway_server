# KnowWay!
the gamified educational resource browser. Get score by reading Wikipedia or reading old books on Polona!

<br>Software Engineering University Project by Dominik Zimny
![KnowWay!](https://i.imgur.com/jlQpgHa.png)

## Basic functionalities
Allows you to host a HTTP server that will contain simple website. Currently implemented functionalities:
- register, login
- search and browse: Wikipedia articles and Polona book scans.
- receiving points for browsing those resources
- show popular resources and top users with the highest number of points
- save information about users locally

## How to run?
### Requirements
```
Python3
Flask_WTF==0.14.3
Flask==1.1.2
wikipedia==1.4.0
WTForms==2.3.1
requests==2.23.0
```
- **Python3** - install from https://www.python.org/downloads/
- **Flask** - ```pip install Flask``` on Windows CMD, or use guide: https://flask.palletsprojects.com/en/1.1.x/installation/
We won't need virtual environment since project doesn't have many dependencies.
- **Flask_WTF** - ```pip install Flask-WTF```
- **requests** - ```pip install requests```
- **WTForms** - ```pip install WTForms```
- **Wikipedia API** - ```pip install wikipedia``` or use guide: https://pypi.org/project/wikipedia/
### Instruction
Add environmental variable at <app directory>/src FLASK_APP=server.py
Run server.py with cmd using ```python.exe <directory>/server.py``` and go ***http://127.0.0.1:5000/*** in your browser.


## Known problems, bugs etc.
Despite web-app working correctly most of the time, there are some things that should be considered for future development:
- it is easy to cheat by sending POST requests that you were browsing resource for some peroid of time (check it on the server-side)
- lack of security while register and login, consider adding a "I am not a robot" checker
- some Polona scans are searched with query that ensures the found books are public, yet API returns some non-public ones, sometimes an error should appear
- Wikipedia pages are loaded on server and then send to the user browsing it, so loading times are a little bit longer than browsing in directly on Wikipedia, same goes for Polona books
- loading a resource for a first time makes it recalculate max points: depending on the resource this may take a little bit longer to load
- data base makes rankings and updates stats every minute, if you are expecting a larger number of users, make it less frequent
