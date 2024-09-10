
import tkinter as tk
from git import Repo
import subprocess
import os
import sys

# Add the directory containing module1 to the Python path
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prompt_def'))
sys.path.insert(0, prompt_path)
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model_interface'))
sys.path.insert(0, prompt_path)

import prompt
import ollama_interface

from prompt import code_review_prompt
from ollama_interface import code_Review_ollama

# Create a new instance of Tkinter
root = tk.Tk()

# Set the title of the window
root.title("Code Review")

code_review_cmd = code_review_prompt()

# Prompt the user for the repository name, path, and branch
repo_name = input("Enter the name of the Git repository: ")
repo_path = input("Enter the path to the Git repository: ")
branch = 'main'

# Create a new instance of the GitPython library
repo = Repo(repo_path)

# Check out the specific branch you want to review
repo.git.checkout(branch)

# Get the list of files in the repository
file_list = repo.git.ls_files().splitlines()
print("Files found:", file_list)

print("Starting code review...")
print(file_list)

algoType = input("Algo Type(GYAN/OLLAMA: ")
model = input("Model(CODELLAMA/LAMMA 3.1/LAMMA 3.1: ")

# Iterate over each file and perform a code review using CodelLLama
for file in file_list:
    if algoType == "GYAN":
        # Run CodelLLama on the file
        codellama_output = subprocess.check_output(["C:/Users/gur25563/AppData/Local/Programs/Ollama/ollama", "run", "codellama", file], text=True)
    else:
        codellama_output = ollama_interface.code_Review_ollama(model,file,code_review_cmd)

    for chunk in codellama_output:
        print(chunk['message']['content'], end='', flush=True)

    print("CodeLlama output received.")
    print(codellama_output)
    # Parse the output of CodelLLama and extract the review comments
    review_comments = []
    for line in codellama_output.splitlines():
         if line.startswith('>>> '):
             review_comments.append(line[4:])

    # Print the review comments for each file
    print("Review comments for " + file)
    print("\n".join(review_comments))

# Create a new instance of Tkinter's Text widget to display the code review results

text = tk.Text(root, height=20, width=80)
text.pack()

# Set the text of the Text widget to the output of CodelLLama
text.insert("end", codellama_output)

# Start the GUI event loop
root.mainloop()
