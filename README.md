# Welcome to baronbale.de

This is the repository containing the code for [baronbale.de](https://baronbale.de) (obviously).

## Development

You want to contribute and run this code locally on your machine? Great! Here is how to get things running.

### Set Up environment

At first, create a venv. Please be aware, that baronbale.de currently has some dependencies which stick us to python3.7.
Might be easy to upgrade, might be not. This is a cleanup task for the future.

```bash
python3.7 -m venv venv
```

Activate venv:

```bash
source venv/bin/activate
```

Then, update some stuff which is not updated automatically.

```bash
pip install -U pip wheel setuptools
```

Now, install all the needed dependencies.

```bash
pip install -r requirements.txt
```

Finally, you need to set some environment variables. open `.env.localDev`, adjust the values to your needs and then run

```bash
source .env.localDev
```

### Run for local development

To run the site on your local machine just make sure you are in the same directory as `manage.py`.

At first you need to make sure your database is migrated to the latest state, you have a place for your media to live and the staticfiles are in place.
```bash
python manage.py migrate

mkdir .media
python manage.py collectstatic
```
After that you can run the server.
```bash
python manage.py runserver
```

## Technical depts

[] Python Version is stuck to 3.7 because of some dependencies (like Pillow)

- Action Item: Dependencies need to upgraded
