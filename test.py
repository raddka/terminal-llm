'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'

import os, sys, re
#from modules.functions import *
from print_color import print
import pandas as pd
from llama_cpp import Llama
from llama_cpp.llama_types import ChatCompletionMessage
from modules.helpers import *

def get_user_input_for_variables(var1_default=5, var2_default=8):
    var1 = input(f"Do you want to change var1? - Default is [{var1_default}] (press Enter to use default): ") or var1_default
    var2 = input(f"Do you want to change var2? - Default is [{var2_default}] (press Enter to use default): ") or var2_default
    
    return var1, var2

# Example usage
var1, var2 = get_user_input_for_variables()

# Now you can use var1 and var2 in your function
print(f"var1: {var1}, var2: {var2}")