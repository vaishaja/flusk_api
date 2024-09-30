import os
import sys

from ollama_interface import codeReview_ollama, codeReview_ollama_wrapper, analyze_changes_with_code_llama

def InitiateCodeReview():
   
    file_path =  r'C:\Users\vaishaja\github_codereview\ToT\code_review_app\src\coverity\bcmdnxwr.c'

# Open and read the file
    with open(file_path, 'r') as file:
        file_content = file.read()
    
        

        #comments = analyze_changes_with_code_llama(files)
    comments = codeReview_ollama_wrapper(file_content)
        
    print(comments)

# Start code review
InitiateCodeReview()