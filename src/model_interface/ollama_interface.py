# ollama_interface.py
import os
import ollama
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
 
# Add the directory containing module1 to the Python path
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prompt_def'))
sys.path.insert(0, prompt_path)
 
from prompt import code_review_prompt
 
model_name = "codellama"
 
def codeReview_ollama(code="", prompt=""):
    response = ollama.chat(model_name, messages=[
      {
        'role': 'user',
        'content': "{0}\n{1}".format(code, prompt),
      },
    ])
 
    return response["message"]["content"]
 
def analyze_changes_with_code_llama(file_changes):
    # Load Code Llama model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
 
    comments = []
    for file in file_changes:
        code     = file['patch']
        inputs   = tokenizer.encode(code, return_tensors='pt')
        outputs  = model.generate(inputs, max_length=512)
        analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)
       
        comment = f"Review for {file['filename']}:\n"
        comment += f"Additions: {file['additions']}\n"
        comment += f"Deletions: {file['deletions']}\n"
        comment += f"Code Llama analysis: {analysis}\n"
        comments.append(comment)
    return comments
 
def codeReview_ollama_wrapper(file_list):
  comments = []
  code_review_cmd = code_review_prompt()
  print("\n Review Started by AI Genie ")
  print(" Number of Files : \n ",len(file_list))
  
  for file in file_list:
     
     
      code     = file['patch']
      print(" File Under Review : ", file['filename'])
 
      codellama_output = codeReview_ollama(code, code_review_cmd)
      print(code)
      comment = f"Review for {file['filename']}:\n"
      comment += f"Additions: {file['additions']}\n"
      comment += f"Deletions: {file['deletions']}\n"
      comment += f"AI Genie analysis: {codellama_output}\n"
      comments.append(comment)
  return comments
 
