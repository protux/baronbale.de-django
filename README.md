# baronbale.de is dead, long live baronbale.de
Hey there. Thank you for your interest in baronbale.de - unfortunately, the banner parser is hard to maintain. I'm extracting zip files and parse arbitrary XML files - who would have guessed this would cause problems? Ok, me, but I thought I'm nice to you so you would be nice to me. This was not the case. 

Someone started to upload bombs - little zip files extracting into multiple GB of data so the whole servers file system was used and other service running on this server died, too. 

This project was started 100 years ago when I was still a student. Today I don't have the time to take care of things. So I have to unfortunately shut this down. But please, if you have more time than me then please go on - use this code, reupload this service under your own domain on your own server. This is GPLv3 Software, go out and have fun.

BEWARE: this was a hobby and no professional software. Test coverage sucks and I started refactoring the code to be more readable and more maintainable, but I never finished. 

**If you like to take over this project:** please feel free to reach out. I will help to onboard you. I will guide you through everything and will do some pair programming session to get you going. Would be great to see someone picking up this project.

So long and thanks for all the fish.
- Nico aka protux (former member of Team baronbale)  

# Welcome to baronbale.de

This is the repository containing the code for [baronbale.de](https://baronbale.de) (obviously).

## Development

You want to contribute and run this code locally on your machine? Great! Here is how to get things running.

### Set Up environment

At first, create a venv.

```bash
python3 -m venv venv
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

At first, you need to make sure your database is migrated to the latest state, you have a place for your media to live
and the staticfiles are in place.

```bash
python manage.py migrate

mkdir .media
python manage.py collectstatic
```

After that you can run the server.

```bash
python manage.py runserver
```
