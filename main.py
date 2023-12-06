import os, sys, json, csv
from modules.helpers import *
from print_color import print
from llama_cpp import Llama

#Import model and initialize
model_name = model_selector()
n_gpu, n_context = llama_args()

llm = Llama(model_path="./models/" + model_name, chat_format="llama-2", n_gpu_layers=n_gpu, n_ctx = n_context)

#LLM Selection + History init
llm_name = char_selector()

with open('llm_config.json', 'r') as file:
    llm_config = json.load(file)
    
#Load existing history
history_path = os.path.join("history", f'history_{llm_name}.csv')
try:
    with open(history_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        history_dict = list(reader)
        for key in history_dict:
            history = ''
            history = history + prompter(key, history_dict[key])
except FileNotFoundError:
    history = ''
    history_dict = []

#Chat
while True:
    role_select = input("Select role - system/user :> ")
    if role_select == 'system':
        system_message = input('System:> ')
        history, history_dict = history_update('system', history, history_dict, system_message)
    
    user_message = input("User:> ")
    if user_message == 'exit':
        sys.exit(0)  
    history, history_dict = history_update('user', history, history_dict, user_message)

    output = llm(prompt=promp_generator(history),
                max_tokens=llm_config["max_tokens"],
                stop=llm_config["stop"],
                temperature=llm_config["temperature"],
                top_p=llm_config["top_p"],
                top_k=llm_config["top_k"],
                min_p=llm_config["min_p"],
                repeat_penalty=llm_config["repeat_penalty"])  
    assistant_message= output["choices"][0]["text"]

    history, history_dict = history_update_print(llm_name,'assistant', history, history_dict, assistant_message)
    print(assistant_message, tag=llm_name, tag_color='magenta', color='cyan')