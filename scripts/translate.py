"""Calls Google Translate API to get translations"""
import os
import requests
import polib
import argparse
from config import API_KEY


def get_arguments():
    if not API_KEY:
        raise ValueError("Please generate a Google API key and paste it in this file. It's needed to authenticate")
    else:
        parser = argparse.ArgumentParser(description="Calls Google Translate API to get translations")
        parser.add_argument("-f", "--file", type=str, help="File to translate. Accepts plain text docs or .po files")
        parser.add_argument("-s", "--source", type=str, help="language to translate from.")
        parser.add_argument("-t", "--target", type=str, nargs="?", default="en", help="language to translate to. default=en")
        return parser.parse_args()

def translate_text(source, target, text):
    data = {"q": text, "source": source, "target": target}
    response = requests.post(f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}", data=data).json()
    if "error" in response:
        raise ValueError(f"Error status with status code: {response['error']['code']} and message: {response['error']['message']}")
    else:
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
                entry.msgstr = translate_text(source, target, entry.msgid)
        pofile.save(f"{path}/{file_name}_{target}.po")

if __name__ == "__main__":
    args = get_arguments()
    start_translation(args)
