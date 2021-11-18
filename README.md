### Todo API

## Table of contents

-   [General info](#general-info)
-   [Features](#features)
-   [API Endpoints](#api-endpoints)
-   [Technologies](#technologies)
-   [Setup](#setup)

## General info<a name="general-info"></a>

Finance API is a REST API built with Flask & SQLAlchemy to operate CRUD operation on a database. The different routes are described below in the API Endpoint section.

## Features<a name="features"></a>

-   Allow user to fetch Todos
-   Allow user to fetch singular Todo
-   Allow user to post Todo
-   Allow user to delete Todo
-   Allow user to update Todo

## API Endpoints<a name="api-endpoints"></a>

After running the server, consult Documentation at :

> http://127.0.0.1:5000/

-   Todos CRUD

    -   Return JSON with all todos
    -   Return JSON with singular todo
    -   Add new todo
    -   Update existing todo
    -   Delete existing todo

Database schema:

![DB Screenshot](https://github.com/antoineratat/github_docs/blob/main/todo_api/Todo%20DB.png?raw=true)

## Technologies<a name="technologies"></a>

Project is created with: Python / Flask

## Setup<a name="setup"></a>

### Import project

```
$ git clone https://github.com/antoineratat/api_todo.git
$ py -3 -m venv venv
$ venv\Script\Activate
$ cd api_todo
$ pip install -r requirements.txt
```

### Create Environnement Variable
```
$ code config.json

{
	"SECRET_KEY": "secret_key",
	"DATABASE_URL": "sqlite:///dbname.db",
	"JWT_SECRET_KEY": "jwt_key"
}

```

### Initialize Database

```
$ venv\Script\Activate
$ python
$ from run import db
$ db.create_all()
$ exit()
```

### Run project

```
$ python run.py
```
