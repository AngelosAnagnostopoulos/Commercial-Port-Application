# Database programming project: Commercial port application
### Authors: "Angelos Anagnostopopulos, Michalis Drosiadis"

This repository is group 42's attempt at creating a functional commercial port application.
The ERD and Relational Schema were created with scalability and efficiency in mind, and were modeled
after already existing online [marine trackers](https://www.vesselfinder.com/el) and [port databases](https://www.marinetraffic.com/).

For this, we prefered MySQL (as opposed to SQLite or mongoDB) as the main way of interacting with our database, 
since it is easy to write and has all the features that suited our application. We used mysql's connector tool
to interact with our Python application, so as to be lazy and not write any more CRUD commands than necessary.

In order to run the Python application, install all packages from _requirements.txt_ and then start the mysql daemon.
```sh
$ pip install -r requirements.txt
$ sudo systemctl start mysql
```
And run _main.py_ from the /src/ directory.
```sh
$ python3 main.py
```
## Presentation Contents

- Microcosm design and implementation (w/ any assumptions made).
- MySQL CRUD commands and Queries. 
- Python application database creation and code presentation.
- Python application GUI and database interraction.

## GUI Images and examples here

## Docker

## Known Issues
