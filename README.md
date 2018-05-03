# Honours Project Backend Server

This server is built using Django framework and contains the API managing collected data from the Airspeck device.

In order to run it, first create a virtual environment. Then, cd into the project folder and install all dependencies using the requirements file and pip:

```bash
cd ./hons_backend/
pip install -r requirements.txt
```

In order to run the server (during development I ran it using port 8080):

```bash
python manage.py runserver <portname>
```

Also, in order for the server to run properly, it should be connected to a PostgreSQL database running on port 5432. During development I ran both the server and the database on localhost.

After starting the database, in order to synchronize the database structure with the server, run: 

```bash
python manage.py migrate
```

