# translate_files


### Requirements
To install requirements to run script:
* pip install -r requirements.txt

To install requirements to run tests (when written)
* pip install -r requirements-test.txt

You'll also need to get a Google API_KEY:

In order to use the Google Translate API, you need an API KEY.
Create a Google account, and navigate to console.cloud.google.com.
In the header there is a dropdown, click it.
A screen should pop up, and there should be a button to create a new project.
Create a new project.
Click the hamburger button in the top left, hover over APIs and Services.
Click Library, and search for the translate API.
Enable the Cloud Translation API, you will need to enter billing info at this point.
The first 500k characters every month are free as of 5/11/22 so it shouldn't incur any cost. 
https://cloud.google.com/translate/pricing
Click the hambuger again, and hover over APIS and Services, and click Identifiers.
Near the top of the screen, there is a button called Create Credentials. Click it.
Create an API Key, and copy it into config file as the API_KEY variable


### Running Translations
To run the translation script follow this format:

python scripts/translate.py -f <file_path> -s <source language>  -t <target language>

In order to translate the included german.txt to english you can run:

python scripts/translate.py -f german.txt -s de

* de is the ISO-639-1 code for the German language https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
* English is the default for target
* a new file called german_en.txt will appear in the same file as the german.txt file
* Path can be ralative to to where the translate.py file is located

### Running Tests
Using pylint:

pylint tests/
