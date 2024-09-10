# gyan_interface.py
import requests

def evaluate_code(file_content):
    infer_url = "http://10.91.237.233:8000/api/infer/llm"
    
    def get_model_name():
        # Please refer GYAN API Documentation v1.1 for model list
        return "ID_GYAN_LLAMA3"

    def get_project_name():
        # Please provide project name of your choice
        return "default"

    prompt = '''
    Please evaluate the following code with the following additional context:\n       
             {{code}} \n         Use the following checklist to guide your analysis:\n        
			 1. Documentation Defects:\n           
			 a. Naming: Assess the quality of software element names.\n           
			 b. Comment: Analyze the quality and accuracy of code comments.\n        
			 2. Visual Representation Defects:\n            
			 a. Bracket Usage: Identify any issues with incorrect or missing brackets.\n            
			 b. Indentation: Check for incorrect indentation that affects readability.\n            
			 c. Long Line: Point out any long code statements that hinder readability.\n         
			 3. Structure Defects:\n            
			 a. Dead Code: Find any code statements that serve no meaningful purpose.\n            
			 b. Duplication: Identify duplicate code statements that can be refactored.\n         
			 4. New Functionality:\n            
			 a. Use Standard Method: Determine if a standardized approach should be used for single-purpose code statements.\n         
			 5. Resource Defects:\n           
			 a. Variable Initialization: Identify variables that are uninitialized or incorrectly initialized.\n           
			 b. Memory Management: Evaluate the program's memory usage and management.\n         
			 6. Check Defects:\n            
			 a. Check User Input: Analyze the validity of user input and its handling.\n         
			 7. Interface Defects:\n            
			 a. Parameter: Detect incorrect or missing parameters when calling functions or libraries.\n         
			 8. Logic Defects:\n           
			 a. Compute: Identify incorrect logic during system execution.\n            
			 b. Performance: Evaluate the efficiency of the algorithm used.\n         
			 Provide your feedback in a numbered list for each category in a tabular format.         
			 At the end of your answer, summarize the recommended changes to improve the quality of the code provided in a tabular format.  
            Also, provide corrected source code with your comments incorporated.\n     '''

    prompt = prompt.replace("{{code}}", file_content)
    
    payload = {
        "prompt": prompt,
        "model_name": get_model_name(),
        "project_name": get_project_name(),
        "prompt_enabled": True,
        "prompt_type": "",
        "prompt_text": ""
    }
    
    response = requests.post(infer_url, json=payload)
    
    return response.json()
