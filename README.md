# Sentence Finder

This application has been designed to show examples of words being used in real sentences for all the supported languages. While being minimal, currently it does the following:

* Search in a database composed of several hundreds of thousands of sentences available for all supported languages (At the current moment, supported languages are English, Spanish and Russian, but the application can add more languages by editing two lines).
* For every result it is possible to hear a spoken version of the sentence, provided by Google's Text to Speech engine or, if available, text to speech engine of the user's operating system.
* Include a management command for importing all phrases for the specified languages (specified languages are arguments in the command line) directly from the [Tatoeba's sentences file in CSV format](https://tatoeba.org/)
* More languages can be added easily and the application can be extended to accomplish additional tasks (speech to text in results, frequency analisys, elearning exercises...).

Note: For best results, it is very recommended to run this application bound to a Postgre SQL database. This application has not been tested with other database systems and due to the source code it is not guaranteed to work under MariaDB/MySQL, Oracle, SQLite (please don't use SQLite, especially if you plan to put several thousands of sentences to the db) and others.

## Demo

You can see a live demo with 3 languages added: Russian, English and Spanish in the following Address: [Go to the demo of this application](https://manuelcortez.net/find_sentences)

## Dependencies

See requirements.txt to see and install automatically all of the dependencies for this project.

* Django >= 1.11.
* django-markdown-deux

## Setup

### download the dataset

Once the application has been placed somewhere in a django project, its URL patterns (located at sentence_finder.urls) have been imported into the main project and migrations were performed (python manage.py makemigrations sentence_finder && python manage.py migrate sentence_finder), you'll need to import the dataset firstly. To do so, you need to download the sentences file from the [Tatoeba downloads page](https://tatoeba.org/downloads) and place the uncompressed CSV file in the django's root directory (where manage.py lives).

### Importing the dataset

The next step is to import the dataset to the database. You'll do that by executing the following command:

> python manage.py import_sentences rus,eng,spa

Where "rus,eng,spa" is the list of language codes (written in ISO 639-3) separated by comma (and without spaces) from where you want to extract phrases. Take into account that more languages you add here, more phrases will be added to the database. In case you want to add a new language (for example, German), you must import its sentences by adding the code for the language in this step, and modify the application's source code a bit later (read below).

You can import the dataset as many times as you wish. The program will clear the sentences table in the database every time a new import starts, so you will not end with dozens of billions of records.

### Adding a new language

If you have imported a new language not covered here, you will need to add it to the forms and text to speech sections of the application, so users will be able to select your new language from the search form, and text to speech will work as expected, respectively. If you haven't imported any new language, you can skip this section.

there are two steps needed to add a new language.

1. In sentence_finder/forms.py, extend the "language" form field to include a new tuple with ("language_code_ISO 639-3, "Language name as read by user").
2. In sentence_finder/views.py, update the "languages" dictionary and add a new key=Value, being key the language code (again, ISO 639-3) and value the language name with the first capital letter (Spanish, English, Russian...).

### Running

> python manage.py runserver

That should be done. The application should run as expected and display the form correctly, including the full list of languages.

### Customization

This application extends a template called base.html. I have included that template (located in sentence_finder/templates/base.html) so the application could work independently as a "pluggable application" for Django. However, you are free (and encouraged) to override base.html to define your own layout.

