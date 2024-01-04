from glob import glob
import os
folder_path = os.path.sep + "models"
files = glob(os.getcwd() + folder_path + "/*.gguf")
print(files)