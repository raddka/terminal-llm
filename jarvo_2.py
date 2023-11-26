# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 21:33:40 2023

@author: ilter
"""
import re
assistant_message = "To use it, your response should include /function [calculator] [3]"
matches = re.findall(r'\[([^]]+)\]', assistant_message)
extracted_info = {}    
function_name = matches[0]
args_str = matches[1]

def calculator(arg_1):
    print(arg_1)
    return arg_1 + 'hello'

if function_name in globals() and callable(globals()[function_name]):
    func_to_call = globals()[function_name]  
    args = [arg.strip() for arg in args_str.split(',')]
    response = func_to_call(*args)
    print(response)