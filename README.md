# A Django Wedding Website and Guest Management System

Live site examples:

- [Standard Wedding Website](http://rowena-and.coryzue.com/)

There is also [a longer writeup on this project here](https://www.placecard.me/blog/django-wedding-website/).

## What's included?

This includes everything we did for our own wedding:

- A responsive, single-page traditional wedding website
- A public RSVP form (name, contact info, attending/not, guest count) right on the homepage
- A complete guest management application (import/export, admin, dashboard) for tracking your own invite list separately
- Guest dashboard

More details on these below.

### The "Standard" Wedding Website

The standard wedding website is a responsive, single-page, twitter bootstrap-based site (using a modified version of
[this theme](https://blackrockdigital.github.io/startbootstrap-creative/)).

It is completely customizable to your needs and the content is laid out in standard django templates. By default it includes:

- A "hero" splash screen for a photo
- A mobile-friendly top nav with scrollspy
- A photo/hover navigation pane
- Configurable content sections for every aspect of your site that you want
- A set of different styles you can use for different sections

![Hero Section of Wedding Website](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/hero-page.png)

### Public RSVP form

Guests RSVP through a plain public form embedded in the homepage's RSVP section - full name, email, phone number,
whether they're attending, and (if so) a guest count. Submissions are saved to the `RSVP` model and visible in the
admin. This is independent of the guest management system below; it doesn't require pre-importing a guest list or
sending anyone a personalized link.

### Guest management

The guest management functionality acts as a central place for you to manage your own invite list separately from
the public RSVP form above (e.g. for tracking who you've decided to invite, meal choices collected some other way,
or your own notes). It includes two data models - the `Party` and the `Guest`.

#### Party model

The `Party` model allows you to group your guests together (e.g. a couple invited as a unit).
You can also add parties that you're not sure you're going to invite using the `is_invited` field.
There's also a field to track whether the party is invited to the rehearsal dinner.

#### Guest model

The `Guest` model contains all of your individual guests.
In addition to standard name/email it has fields to represent whether the guest is a child (for kids meals/pricing differences),
whether they're attending, and what meal they're having - though nothing in the app currently writes to these from
a public-facing page; they're meant to be maintained via the admin/CSV import based on however you collect that info.

#### Excel import/export

The guest list can be imported and exported via excel (csv).
This allows you to build your guest list in Excel and get it into the system in a single step.
It also lets you export the data to share with others or for whatever else you need.

See the `import_guests` management command for more details and `guests/tests/data` for sample file formats or see the customization section below.

### Guest dashboard

The guest dashboard gives you a quick view of your guest-list numbers: who's pending, who's coming, who's not, meal
breakdowns, and who's attending without a meal selected yet.

Just access `/dashboard/` from an account with admin access. Your other guests won't be able to see it.

![Wedding Dashboard](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/wedding-dashboard.png)

### Other details

You can easily hook up Google analytics by editing the tracking ID in `google-analytics.html`.


## Installation

This is developed for Python 3 and Django 4.1.

It's recommended that you setup a virtualenv before development.

Then just install requirements, migrate, and runserver to get started:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If you run into Python errors, try to replace `python` with `python3`.

You can now visit your site at `http://localhost:8000/`.

The dashboard and admin interface are available at `http://localhost:8000/dashboard/` and `http://localhost:8000/admin/`. 
Use the superuser created in step three of the commands above.


### Database
The default setup of this project uses a SQLite database, which is persisted on the file system. If you want to use another
database you can change the `DATABASES` config option in the `settings.py` file. This file already contains an example
configuration on how to use the [Postgres](https://www.postgresql.org/) database specified in the docker-compose file.

### Docker
You can also run the project using [Docker](https://www.docker.com/). To build the image and run the container you can run:
```bash
docker build -t django-wedding-website .
docker run -it -p 8080:8080 \
      -e DJANGO_SUPERUSER_PASSWORD=changeme \
      -e DJANGO_SUPERUSER_USERNAME=admin \
      -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
      django-wedding-website
```
You can now visit your site at `http://localhost:8080`

#### Docker Compose
To run the project with a Postgres database, you can
- Change the `DATABASES` configuration in `settings.py` to use the Postgres database
- Start the Postgres Database and the project container with `docker-compose up --build`
- You can now visit your site at `http://localhost:8080`

> Note that if you want to make a production deployment with Docker you need to backup the SQLite or Postgres database!

## Customization

I recommend forking this project and just manually modifying it by hand to replace everything with what you want.
Searching for the text on a page in the repository is a great way to find where something lives.

Some things are already customizable thanks to the use of variables. 
Copy `bigday/localsettings.py.template` to `bigday/localsettings.py` and edit the values.
You definitely need to change the `SECRET_KEY` to a new secure value.

`localsettings.py` is excluded from Git, so you won't accidentally submit your personal data to a public repository.

### Sending email

There is no built-in outbound emailing (no invitation or save-the-date emails) - guests RSVP directly through the
public form on the homepage instead. The app still uses Django's email framework generally (e.g. `MAIL_BACKEND` in
`bigday/settings.py`, toggleable between `console` and `smtp`), in case you want to add your own notification emails.

### Email addresses

The site's "Contact us" section shows `DEFAULT_WEDDING_REPLY_EMAIL`, which you can set in `bigday/localsettings.py`
(see `Customization`) along with `DEFAULT_WEDDING_EMAIL`.

### Import guests

To manage your own invite list separately from the public RSVP form, you can import guests via CSV.
The import method expects a CSV file with the following header:

`party_name,first_name,last_name,party_type,is_child,category,is_invited,email`

A sample line could be:

`Party Name,Phred,McPhredson,formal,n,Groom,y,email@domain.tld`

The import command is:

```bash
python manage.py import_guests guestList.csv
```

If you want to add more guests to the list, simply create a new CSV and rerun the command.

### Other customizations

If you want to use this project for your wedding but need help getting started just [get in touch](http://www.coryzue.com/contact/) or make an issue
for anything you encounter and I'm happy to help.

I haven't built out more complete customization docs yet because I wasn't sure anyone would be interested in this,
but will add to these instructions whenever I get questions!

-Cory
