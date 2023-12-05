import os, sys, json, csv
from modules.helpers import *
from print_color import print
from llama_cpp import Llama
from transformers import pipeline
sys.path.append(os.getcwd())

#Import model and initialize
model_name = model_selector()

if model_name.endswith(".gguf"):
    model_type = 'gguf'
    n_gpu, n_context = llama_args()
    llm = Llama(model_path="./models/" + model_name, chat_format="llama-2", n_gpu_layers=n_gpu, n_ctx = n_context)
else:
    model_type = 'transformer'
    models_path = os.path.join(os.getcwd(),'models')
    generator = pipeline(model= os.path.join(models_path, model_name),task="text-generation",device_map="auto",)

#LLM Selection + History init
llm_name = char_selector()

if model_type == 'gguf':
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

    if model_type == 'gguf':
        output = llm(prompt=promp_generator(history),
                    max_tokens=llm_config["max_tokens"],
                    stop=llm_config["stop"],
                    temperature=llm_config["temperature"],
                    top_p=llm_config["top_p"],
                    top_k=llm_config["top_k"],
                    min_p=llm_config["min_p"],
                    repeat_penalty=llm_config["repeat_penalty"])  
        assistant_message= output["choices"][0]["text"]
    else:
        output = generator(promp_generator(history), max_length=2048, num_return_sequences=1, temperature=1.0)  
        lines = output[0]["generated_text"].split('\n')
        last_assistant_index = max([i for i, line in enumerate(lines) if 'assistant' in line])
        assistant_message = ''.join(lines[last_assistant_index + 1:])

    history, history_dict = history_update_print(llm_name,'assistant', history, history_dict, assistant_message)
    print(assistant_message, tag=llm_name, tag_color='magenta', color='cyan')