import os, sys, re
from modules.functions import *
from print_color import print
import pandas as pd
from openai import OpenAI
from os import getenv

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=getenv("OPENROUTER_API_KEY"),)

def response_generator(message_dict):
    completion = client.chat.completions.create(model="nousresearch/nous-capybara-34b", messages=message_dict)
    response = completion.choices[0].message.content
    return response
    
#LLM Selection + History init
print(os.listdir('./history'))
llm_name = input("Select LLM:> ")
if llm_name == 'exit':
        sys.exit(0)

try:
    history = []
    history_df = pd.read_csv('.\history\history_' + llm_name + '.csv')
    history_dict = history_df.to_dict(orient='records')
    history = history + history_dict
    for key in history:
        print(history[key], tag=key, tag_color='magenta', color='cyan')
except:
    history = []

def history_update(list_name):
    df = pd.DataFrame(list_name, columns=['role','content'])
    df.to_csv('.\history\history_' + llm_name + '.csv', index=False)

#Chat
while True:
    role_select = input("Select role - system/user :> ")
    if role_select == 'system':
        system_message = input('System:> ')
        history.append({"role": "system", "content": system_message})
    if role_select == 'clear':
        history = []    
    user_message = input("Raddka:> ")
    if user_message == 'exit':
        sys.exit(0)
    history.append({"role": "user", "content": user_message})
    assistant_message = response_generator(history)
    
    history.append({"role": "assistant", "content": assistant_message})
    history_update(history)
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
        
        history.append({"role": "system", "content": response})
        assistant_message = response_generator(history)        
        history.append({"role": "assistant", "content": assistant_message})
        history_update(history)  
        print(assistant_message, tag=llm_name, tag_color='magenta', color='cyan')