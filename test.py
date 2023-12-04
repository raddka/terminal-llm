'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'

import os, sys, re
#from modules.functions import *
from print_color import print
import pandas as pd
from llama_cpp import Llama
from llama_cpp.llama_types import ChatCompletionMessage
from modules.helpers import *

file = model_selector()
print("You've selected: " + file)
