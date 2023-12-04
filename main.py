import os, sys, re
from modules.functions import *
from modules.helpers import *
from print_color import print
import pandas as pd
from llama_cpp import Llama
from llama_cpp.llama_types import ChatCompletionMessage

#Import model and initialize
model_name = model_selector()
n_gpu, n_context = llama_args()

llm = Llama(model_path="./models/" + model_name, chat_format="llama-2", n_gpu_layers=n_gpu, n_ctx = n_context)

#LLM Selection + History init
llm_name = char_selector()

#Load existing history
try:
    history_df = pd.read_csv('.\history\history_' + llm_name + '.csv')
    history_dict = history_df.to_dict(orient='records')
    for key in history_dict:
        history = ''
        history = history + prompter(key, history_dict[key])
        history_dict = []
        history_dict = history_dict + pd.read_csv('.\history\history_' + llm_name + '.csv').to_dict(orient='records')        
except:
    history = ''
    history_dict = []

#Chat
while True:
    role_select = input("Select role - system/user :> ")
    if role_select == 'system':
        system_message = input('System:> ')
        history = history + prompter('system', system_message)
        history_dict.append({"role": "system", "content": system_message})
    user_message = input("User:> ")
    if user_message == 'exit':
        sys.exit(0)    
    if role_select == 'clear':
        history = []  
    history = history + prompter('user', user_message)
    history_dict.append({"role": "user", "content": user_message})
    output = llm(prompt=promp_generator(history), max_tokens=1024, stop=["<|im_end|>"], temperature=1.0, top_p= 1.0, top_k= 0, min_p= 0.1, repeat_penalty= 1.0)
    assistant_message = output["choices"][0]["text"]
    history = promp_saver(history, assistant_message)
    history_dict.append({"role": "assistant", "content": assistant_message})
    history_update(llm_name, history_dict)
    print(assistant_message, tag=llm_name, tag_color='magenta', color='cyan')
        
    if '/function' in assistant_message:
        matches = re.findall(r'\[([^]]+)\]', assistant_message)
        extracted_info = {}    
        function_name = matches[0]
        try:
            args_str = matches[1]
            if function_name in globals() and callable(globals()[function_name]):
                func_to_call = globals()[function_name]  
                args = [arg.strip() for arg in args_str.split(',')]
                response = func_to_call(*args)
            else:
                response = 'Function not found'
        except:
            if function_name in globals() and callable(globals()[function_name]):
                func_to_call = globals()[function_name]
                response = func_to_call()
            else:
                response = 'Function not found'        
        
        history = history + prompter('system', response)
        history_dict.append({"role": "system", "content": response})

        output = llm(prompt=promp_generator(history), max_tokens=1024, stop=["<|im_end|>"], temperature=1.0, top_p= 1.0, top_k= 0, min_p= 0.1, repeat_penalty= 1.0)
        assistant_message = response['choices'][0]['message']['content']
        print(assistant_message, tag='System', tag_color='yellow', color='white')
        assistant_message = output["choices"][0]["text"]

        history = promp_saver(history, assistant_message)
        history_dict.append({"role": "assistant", "content": assistant_message})
        history_update(llm_name, history_dict)
        print(assistant_message, tag=llm_name, tag_color='magenta', color='cyan')