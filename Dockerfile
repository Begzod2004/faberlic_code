# base image  
FROM python:3.8
# setup environment variable  
ENV SECRET_KEY=django-insecure-*#3kq$q!bmd@=7!=&e!sxjsb1#g)t_q+)5yrh2k00s*f707r!l
ENV DATABASE_URL=postgres://b2bdb_user:z1aUKb0SjzBCmnErf2OvCEJTXEA69Rfn@dpg-cj5298c5kgrc73frc8i0-a.oregon-postgres.render.com/b2bdb
# where your code lives  

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]    