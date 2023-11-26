import os

def create_file(file_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, "workspace")
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        return "File already exists"
    else:
        with open(file_path, 'w') as file:
            file.write("#Created by Hermes")
            return "File created"
        
def create_idea(idea_name, content):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, "workspace")
    folder_path = os.path.join(current_directory, "ideas")
    file_name = idea_name + '.txt'
    file_path = os.path.join(folder_path, file_name )
    if os.path.exists(file_path):
        return "Idea already exists"
    else:
        with open(file_path, 'w') as file:
            file.write("### System: Idea Created by Hermes \n")
            file.write(content)
            return "Idea created"    

def load_idea(idea_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, "workspace")
    folder_path = os.path.join(current_directory, "ideas")
    file_name = idea_name + '.txt'
    file_path = os.path.join(folder_path, file_name )
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            idea_content = file.read()
            return idea_content
    else:
        return "Idea not found" 

def delete_idea(idea_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, "workspace")
    folder_path = os.path.join(current_directory, "ideas")
    file_name = idea_name + '.txt'
    file_path = os.path.join(folder_path, file_name )
    if os.path.exists(file_path):
        os.remove(file_path)
        return "Idea deleted"
    else:
        return "Idea not found"    

def list_ideas():
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, "workspace")
    folder_path = os.path.join(current_directory, "ideas")
    if os.path.exists(folder_path):       
        return os.listdir()
    else:
        return 'No existing ideas.'