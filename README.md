# TreasureHunt Game

TreasureHunt is a game which can be played using API. The idea is to find treasure location.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.  

### Prerequisites

* docker
* docker-compose
* pipenv (for linting and running tests)
* (recommended) pyenv

### Installing

Add and edit `.env` file.

```shell-script
TREASUREHUNT_SECRET_KEY="YOUR-SECRET-SECRET"
```

All possible env variables in [settings](treasurehunt/settings.py)

Run treasurehunt service

```shell-script
docker-compose up treasurehunt
```

#### Interacting

OpenAPI http://localhost:8069/docs

[Connecting to follow the game events websocket](examples/ws_client.py)

### Setting up dev environment 

Install dev packages

```shell-script
pipenv isntall -d
```

#### Linting

```shell-script
make lint
```

#### Running tests

```shell-script
make test
```

or alternatively

```shell-script
make test-unit 
make test-functional
```

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production 
