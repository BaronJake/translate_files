"""Calls Google Translate API to get translations"""
import os
import requests
import polib
import argparse
from config import API_KEY


"""
In order to use the Google Translate API, you need an API KEY.
Create a Google account, and navigate to console.cloud.google.com.
In the header there is a dropdown, click it.
A screen should pop up, and there should be a button to create a new project.
Create a new project.
Click the hamburger button in the top left, hover over APIs and Services.
Click Library, and search for the translate API.
Enable the Cloud Translation API, you will need to enter billing info at this point.
The first 500k characters every month are free as of 5/11/22 so it shouldn't incur any cost. https://cloud.google.com/translate/pricing
Click the hambuger again, and hover over APIS and Services, and click Identifiers.
Near the top of the screen, there is a button called Create Credentials. Click it.
Create an API Key, and copy it into this script as the API_KEY variable
Also need to install polib
"""


def get_arguments():
    if not API_KEY:
        raise ValueError("Please generate a Google API key and paste it in this file. It's needed to authenticate")
    parser = argparse.ArgumentParser(description="Calls Google Translate API to get translations")
    parser.add_argument("-f", "--file", type=str, help="File to translate. Accepts plain text docs or .po files")
    parser.add_argument("-s", "--source", type=str, help="language to translate from.")
    parser.add_argument("-t", "--target", type=str, nargs="?", default="en", help="language to translate to. default=en")
    return parser.parse_args()

def translate_text(source, target, text):
    """Sends request to Google Translate API and returns translated text"""
    data = {"q": text, "source": source, "target": target}
    response = requests.post(f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}", data=data).json()
    if "error" in response:
        raise ValueError(f"Error status with status code: {response['error']['code']} and message: {response['error']['message']}")
    return response["data"]["translations"][0]["translatedText"]

def start_translation(args):
    """Opens file, translates all text and writes output file"""
    file = args.file
    source = args.source
    target = args.target
    path = "".join(file.split("/")[:-1])
    if not path:
        path = os.getcwd()
    file_name, file_ext = file.split("/")[-1].split(".")
    if file_ext != ".po":
        with open(file, "r") as original_file:
            original_data = original_file.read().split("\n")
        with open(f"{path}/{file_name}_{target}.{file_ext}", "w") as outfile:
            for line in original_data:
                translated_text = translate_text(source, target, line)
                outfile.write(f"{translated_text}\n")
    else:
        pofile = polib.pofile(file)
        for entry in pofile:
            if entry.msgid and not entry.msgstr:
                entry.msgstr = translate_text(entry.msgid)
        pofile.save(f"{path}/{file_name}_{target}.po")

if __name__ == "__main__":
    args = get_arguments()
    start_translation(args)
