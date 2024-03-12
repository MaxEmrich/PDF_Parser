from src.parser_class import PDF_PARSER
import os
import src.gui as gui
import json
import shutil
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


gui.start_gui_loop()
user_input_text = None
file_path = None

def get_downloads_folder():
    home = os.path.expanduser("~")
    if os.name == 'posix':  # Unix-based systems like macOS
        return os.path.join(home, "Downloads")
    elif os.name == 'nt':   # Windows
        return os.path.join(home, "Downloads")
    else:
        return None  # Unsupported OS

downloads_folder = get_downloads_folder()

#clean up user input text:
def cleanUpText(original_input_text) -> str:
    cleaned_text = original_input_text.strip()
    cleaned_text = cleaned_text.lower() 
    return cleaned_text

def cleanUpFileName(file_path) ->  str:
    cleaned_file_name = file_path.lower()
    cleaned_file_name = cleaned_file_name.strip()
    cleaned_file_name = cleaned_file_name.split('/')[-1] # use [-1] to select last element of the array, which is always the file name after the split
    return cleaned_file_name 
    
def addFileToDir(current_dir):
    documents_folder = os.path.join(current_dir, "document_uploads")
    os.makedirs(documents_folder, exist_ok=True)
    destination_path = os.path.join(documents_folder, os.path.basename(file_path)) 
    shutil.copy(file_path, destination_path)

with open('data.json', 'r+') as file:
    data = json.load(file)
    user_input_text = data["user_input_text"]
    file_path = data["fileName"]
    file.truncate(0)
    file.close()

clean_text = cleanUpText(user_input_text)
clean_file_name = cleanUpFileName(file_path)
print(clean_file_name)

current_dir = os.path.dirname(__file__)
addFileToDir(current_dir=current_dir)

# Assuming your main file is in the same directory as the PDF file
parser_object = PDF_PARSER(file_path)

new_reader = parser_object.create_reader(directory=current_dir)

pages_with_keyphrase = []

for page_number in range(len(new_reader.pages)):
    page = new_reader.pages[page_number]
    page_text = page.extract_text()
    lines = page_text.split("\n")
    for line in lines:
        if clean_text in line:
            pages_with_keyphrase.append(page_number)

print(pages_with_keyphrase)
print(len(pages_with_keyphrase))

new_writer = parser_object.create_writer()
for page_number in pages_with_keyphrase:
    new_writer.add_page(new_reader._get_page(page_number))
    
document_path = os.path.join(current_dir, downloads_folder, "cleaned_" + clean_file_name)
with open(document_path, "wb") as finished_file:
    new_writer.write(finished_file)

if os.path.join(current_dir, downloads_folder, "cleaned_" + clean_file_name):
    os.remove((os.path.join(current_dir, "document_uploads", clean_file_name)))




