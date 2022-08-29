"""Calls Google Translate API to get translations"""
import os
import argparse
import requests
import polib
from .resources.config import API_KEY


def get_arguments():
    """gets arguments passed in commandline"""
    if not API_KEY:
        raise ValueError(
            "Please generate a Google API key and paste it in this file. "
            "It's needed to authenticate"
        )
    parser = argparse.ArgumentParser(
        description="Calls Google Translate API to get translations"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="File to translate. Accepts plain text docs or .po files",
    )
    parser.add_argument("-s", "--source", type=str, help="language to translate from.")
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        nargs="?",
        default="en",
        help="language to translate to. default=en",
    )
    return parser.parse_args()


def translate_text(source, target, text):
    """Calls Google Translate API to translate text"""
    data = {"q": text, "source": source, "target": target}
    response = requests.post(
        f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}",
        data=data,
    )
    if response.status_code != 200:
        raise ConnectionError(f"Status code: {response.status_code}")
    response = response.json()
    if "error" in response:
        raise ValueError(
            f"Error status with status code: "
            f"{response['error']['code']} and "
            f"message: {response['error']['message']}"
        )
    return response["data"]["translations"][0]["translatedText"]


def start_translation(arguments):
    """Opens file, translates all text and writes output file"""
    file = arguments.file
    source = arguments.source
    target = arguments.target
    path = "".join(file.split("/")[:-1])
    if not path:
        path = os.getcwd()
    file_name, file_ext = file.split("/")[-1].split(".")
    if file_ext != ".po":
        with open(file, "r", encoding="utf-8") as original_file:
            original_data = original_file.read().split("\n")
        with open(f"{path}/{file_name}_{target}.{file_ext}", "w", encoding="utf-8") as outfile:
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
