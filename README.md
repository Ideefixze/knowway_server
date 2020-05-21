# KnowWay!
the gamified educational resource browser <br>Software Engineering University Project by Dominik Zimny
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
Flask
wikipedia python API
```
**Python3** - install from https://www.python.org/download/releases/3.0/
**Flask** - ```pip install Flask``` on Windows CMD, or use guide: https://flask.palletsprojects.com/en/1.1.x/installation/
We won't need virtual environment since project doesn't have many dependencies.
**Wikipedia API** - ```pip install Wikipedia``` or use guide: https://pypi.org/project/wikipedia/


## Known problems, bugs etc.
Despite web-app working correctly most of the time, there are some things that should be considered for future development:
- it is easy to cheat by sending POST requests that you were browsing resource for some peroid of time (check it on the server-side)
- lack of security while register and login, consider adding a "I am not a robot" checker
- some Polona scans are searched with query that ensures the found books are public, yet API returns some non-public ones, sometimes an error should appear
- Wikipedia pages are loaded on server and then send to the user browsing it, so loading times are a little bit longer than browsing in directly on Wikipedia, same goes for Polona books
- loading a resource for a first time makes it recalculate max points: depending on the resource this may take a little bit longer to load
- data base makes rankings and updates stats every minute, if you are expecting a larger number of users, make it less frequently
