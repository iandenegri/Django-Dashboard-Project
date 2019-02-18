# What is this?
Django project built to test and try various different techniques and applications that can be done in Django.

## Some information
Most of the work on this project went towards developing views and utilities for the site rather than the appearance of the site. I'm not a front end or UI designer (though I'd like to learn how do that kind of work at some point) so I wanted to spend more time towards bettering what I currently do. I could and should make the front end more aesthetically pleasing since a lot of it is just slapped together and uses front end elements that other users have developed. 

## How does it work?
1. Pull the code to your machine.
1. Use the requirements.txt to build a virtual env with all the libraries needed to run the code.
1. Run the virtual env and then go into the source folder.
1. Update the secret key in the settings.py
1. Create a superuser profile `python manage.py createsuperuser`
1. You can now just do `python manage.py runserver`
1. Log in as your user at localhost:8000/admin/
1. You can now access the site at localhost:8000/

## What are some features?
* Web scraping to put together a "news" feed for you.
    * The news is scraped from The Onion, saved to the database for the project and then presented to the user on the dashboard.
    * To keep the user from assaulting The Onion with scrapes there is a 1 hour timer where the user can't scrape.
* You can write notes to yourself on your dashboard with a link and image. :D
* The site has an API end point built into the site just for the sake of API end point practice.
    * There's also a bar graph that uses that end point to show it working.
* On the dashboard the user can click a link that lets the user check stock prices and trends. This isn't built using anything specific to Django but is more so an integration of another library to do that.

## What's still needed?
* I need to create a login page that isn't tied to the admin panel.
* There should also be a sign up page in case I want users to be able to use this too...
* A nicer UI.
* Maybe a friends list so that users can add each other and see each other's notes. This could give the notes feature real use. Right now it's kind of just a solution for an issue that existed like 10 years ago when applications weren't linked together and you couldn't access notes and documents from other devices.
* A gitignore file and cleaning up the repo.