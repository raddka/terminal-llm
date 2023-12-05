'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'

import os, sys, re
#from modules.functions import *
from print_color import print
from modules.helpers import *

def model_selector():
    folder_path = "models"
    extension = ".gguf"
    gguf_files = [file for file in os.listdir(os.path.join(os.getcwd(),folder_path)) if file.endswith(extension)]
    folders = [f for f in os.listdir(os.path.join(os.getcwd(), folder_path)) if os.path.isdir(os.path.join(folder_path, f))]
    files = folders + gguf_files
    if not files:
        print(f"No models found in the folder.")
        return

    print("Available models:")
    for i, file in enumerate(files, start=1):
        print(f"[{i}] {file}")
    selected_file = None

    try:
        choice = int(input("Enter the number of the model you want to select: "))
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    if selected_file is not None:
        print(f"You selected: {selected_file}")
    return selected_file

file_name = model_selector()
print(file_name)