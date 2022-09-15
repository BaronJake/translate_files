import os
import argparse
import easyocr

def get_arguments():
    """gets arguments passed in commandline"""
    parser = argparse.ArgumentParser(
        description="Counts the number of characters in a file"
    )
    parser.add_argument(
        "-f",
        "--folder",
        type=str,
        help="Folder of image files to extract text from",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        help="Language of image text. Helps OCR read correctly"
    )
    return parser.parse_args()

def get_text_from_images(arguments):
    folder = arguments.folder
    source_lang = arguments.source
    list_of_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    
    list_of_files.remove(os.path.join(root, "ocr_text.txt"))
    number_of_files = len(list_of_files)
    reader = easyocr.Reader([source_lang], gpu=False)
    with open(f"{folder}/ocr_text.txt", "a", encoding="utf-16") as ocr_file:
        for file_num, file in enumerate(list_of_files):
            print(f"Working on file {file_num + 1}/{number_of_files}")
            text = reader.readtext(file, detail=0, paragraph=True)
            ocr_file.write("\n".join(text))

    
if __name__ == "__main__":
    args = get_arguments()
    get_text_from_images(args)