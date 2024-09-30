import os
import sys
#import prompt
#import ollama_interface
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model_interface'))
sys.path.insert(0, prompt_path)

from ollama_interface import code_review_ollama_wrapper_static_analysis
def list_files(directory):
    """List all files in the given directory."""
    try:
        files = os.listdir(directory)
        return [f for f in files if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print("Directory not found.")
        return []

def read_file(file_path):
    """Read and return the content of the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    repo_directory = input("Enter the path to your local repository: ")
    
    # List files in the directory
    files = list_files(repo_directory)
    print(files)
    
    if not files:
        print("No files found in the repository.")
        return
    
    # Display the list of files
    print("Files in the repository:")
    file_list = [os.path.join(repo_directory, file)  for file in files]
    comments = code_review_ollama_wrapper_static_analysis(file_list)
    print(comments)
    
   

if __name__ == "__main__":
    main()
