# B2B Project

## Project Overview

![python](https://img.shields.io/badge/-python-grey?style=for-the-badge&logo=python&logoColor=white&labelColor=306998)
![django](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![postgresql](https://img.shields.io/badge/postgre-SQL-%23000.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![linux](https://img.shields.io/badge/linux-grey?style=for-the-badge&logo=linux&logoColor=white&labelColor=072c61)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

### Language: python 3.8 +

### Frameworks : Django 4+, DjangoRestFramework 3.12 +

### Database : postgresql 12+

### Project Setup

#### Create Database

```bash
>>> create role b2b_db with login password '2404';
>>> create database b2b_db with owner ulov_user;
```

#### Django install

```bash
>>> git clone https://gitlab.com/00009998id/notify.git
>>> virtualenv .venv
>>> source .venv/bin/activate
>>> pip install -r requirements/local.txt
>>> python manage.py migrate --settings=config.settings.local
>>> python3 manage.py runserver --settings=config.settings.local
```
