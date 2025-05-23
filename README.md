# Med-Rag

This project is a medical chatbot

## Requirements

- python 3.13.2 or later


### install Python using MiniConda

1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/main)

2) Create a new environment using following command:
```bash
$ conda create -n Medical-rag-app python 3.13.2
```

3) Activate the environment
```bash
$ conda activate Medical-rag-app
```

## Installation

```bash
$ pip install -r requirements.txt
```

#### setup the environment variables

``` bash
$ cp .env.example .env

```

set your environment variables in the `.env` file , Like `Chatbot APIs` values




## Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
```
- update `.env` with your credentials





## Run FastAPI Server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 500
```
