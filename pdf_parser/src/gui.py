from tkinter import *
import customtkinter
from tkinter import filedialog
import json
import shutil
import os

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("1080x720")
app.title("Supply Distro App")
app.resizable = True
app.filename = None
app.userInputText = None

# Defining functions for events

def addFileToDir():
    documents_foler = os.path.join(os.path.dirname(__file__), "../", "document_uploads")
    os.makedirs(documents_foler, exist_ok=True)
    destination_path = os.path.join(documents_foler, os.path.basename(app.filename)) 

def upload_clicked(): 
    app.userInputText = userInputField.get()
    if app.filename != None:
        addFileToDir()
        data = {
            "fileName": app.filename,
            "user_input_text": app.userInputText
        }
        with open('data.json', 'w') as file:
            try:
                json.dump(data, file)
                print("Data has been pushed to json file: data.json")
                file.close()
            except:
                print("Error! data could not be added to json. File may not be empty")
        on_upload_complete()
    return 0


def on_upload_complete():
    app.withdraw()  # Hide the window
    app.quit()      # Stop the event loop

def access_files():
    app.filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("pdf files", "*.pdf"),))
    return app.filename


# Adding UI elements 
title = customtkinter.CTkLabel(
    app, text="Upload your pdf file"
    )
submit_button = customtkinter.CTkButton(
    app, text="submit the text to be parsed", text_color="black", fg_color="red", width=20, height=30, command=upload_clicked
    )
access_files_button = customtkinter.CTkButton(
    app, text="access your files to upload a pdf", text_color="black", width=30, height=30, command=access_files
    )
userInputField = customtkinter.CTkEntry(
    app, width=350, height=40
    )

userInputField.state=NORMAL

title.pack(padx=10, pady=10)
access_files_button.pack(pady=50, padx=20)
userInputField.pack(pady=30)
submit_button.pack(padx=20, pady=5)

# Run app continuously (Note: Always run mainloop() AFTER all elements are defined)
def start_gui_loop():
    app.mainloop()