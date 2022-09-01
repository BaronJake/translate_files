import os
import argparse
import polib

def get_arguments():
    """gets arguments passed in commandline"""
    parser = argparse.ArgumentParser(
        description="Counts the number of characters in a file"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="File to translate. Accepts plain text docs or .po files",
    )
    return parser.parse_args()


def count_chars(arguments):
    """Opens file, prints number of chars"""
    file = arguments.file
    num_chars = 0
    path = "".join(file.split("/")[:-1])
    if not path:
        path = os.getcwd()
    _, file_ext = file.split("/")[-1].split(".")
    if file_ext != ".po":
        with open(file, "r", encoding="utf-8") as original_file:
            original_data = original_file.read().split("\n")
        for line in original_data:
            num_chars += len(line)
    else:
        pofile = polib.pofile(file)
        for entry in pofile:
            if entry.msgid and not entry.msgstr:
                num_chars += len(entry.msgid)
    print(num_chars)

if __name__ == "__main__":
    args = get_arguments()
    count_chars(args)
