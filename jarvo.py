import requests
import os, sys, json, re
import pandas as pd
from modules.helpers import colored
from modules.hermes_functions import create_file, create_idea, load_idea, delete_idea, list_ideas

url = "http://127.0.0.1:5000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

history = []

history_df = pd.read_csv('history.csv')
history_dict = history_df.to_dict(orient='records')
history = history + history_dict

color = "cyan"

def history_update(role, message, list_name, filename):
    list_name.append({"role": role, "content": message})
    df = pd.DataFrame(list_name, columns=['role','content'])
    df.to_csv(filename, index=False)

while True:
    user_message = input("Raddka:> ")
    if user_message == 'exit':
        sys.exit(0)
    history.append({"role": "user", "content": user_message})
    data = {
        "mode": "instruct",
        "messages": history
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    history_update("assistant",assistant_message, history, 'history.csv')
    sys.stdout.write(colored(">Hermes: " + assistant_message + "\n", color))
    sys.stdout.flush()
        
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
        sys.stdout.write(colored(">Notification: " + response + "\n", "green"))
        sys.stdout.flush()
        
        history.append({"role": "notification", "content": response})
        data = {"mode": "instruct","messages": history}
        response = requests.post(url, headers=headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        history_update("assistant",assistant_message, history, 'history.csv')    
        cur = ">Hermes: " + assistant_message + "\n"
        sys.stdout.write(colored(cur, "cyan"))
        sys.stdout.flush()
    