#For the future.
import os, csv

def model_selector():
    folder_path = "\models"
    extension = ".gguf"
    files = [file for file in os.listdir(os.getcwd() + folder_path) if file.endswith(extension)]
    if not files:
        print(f"No {extension} models found in the folder.")
        return

    print("Available models:")
    for i, file in enumerate(files, start=1):
        print(f"[{i}] {file}")
    
    try:
        choice = int(input("Enter the number of the model you want to select: "))
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    print(f"You selected: {selected_file}")
    return selected_file

def llama_args(n_gpu_layers_default=-1, n_ctx_default=16386):
    var1 = input(f"Change n_gpu_layers? - Default [{n_gpu_layers_default}] (press Enter to use default): ") or n_gpu_layers_default
    var2 = input(f"Change n_ctx? - Default [{n_ctx_default}] (press Enter to use default): ") or n_ctx_default
    
    return int(var1), int(var2)

def char_selector():
    folder_path = "\history"
    extension = ".csv"
    shared_string = "history_"

    files = [file for file in os.listdir(os.getcwd() + folder_path) if file.endswith(extension)]
    if not files:
        choice_new = input("Provide a name for the new Char:")
        return choice_new

    print("Available chars:")
    for i, file in enumerate(files, start=1):
        display_name = file.replace(shared_string, "").replace(extension, "")
        print(f"[{i}] {display_name}")

    choice = input("Enter the number of the char you want or write the name for a new char: ")
    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(files):
            selected_char = files[choice - 1].replace(shared_string, "").replace(extension, "")
            print(f"You selected: {selected_char}")
            return selected_char
        else:        
            print("Invalid input. Please enter a correct number.")
            return None
    except:
        print(f"You've created: {choice}")
        return choice


def prompter(role, content):
    message = '<|im_start|>'+ role +' \n' + content + '<|im_end|> \n'
    return message

def promp_generator(content):
    prompt = content +  '<|im_start|>assistant \n'
    return prompt

def history_update(role, conversation, conversation_dict, content):
    conversation += prompter(role, content)
    conversation_dict.append({"role": role, "content": content})
    return conversation, conversation_dict

def history_update_print(file_name, role, conversation, conversation_dict, content):
    conversation += prompter(role, content)
    conversation_dict.append({"role": role, "content": content})
    keys = conversation_dict[0].keys()
    history_path = os.path.join("history", f'history_{file_name}.csv')
    with open(history_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(conversation_dict)
    return conversation, conversation_dict