import os
import sys

# Add the directory containing module1 to the Python path
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model_interface'))
sys.path.insert(0, prompt_path)
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'git_interface'))
sys.path.insert(0, prompt_path)

from ollama_interface import codeReview_ollama, codeReview_ollama_wrapper, analyze_changes_with_code_llama
from gitHub_interface import validate_GitRepoInfo, get_pull_request_files, post_review_comments


def InitiateCodeReview():
    # https://github.com/taskflow/taskflow?tab=License-1-ov-file
    # Git Repo Owner: "Tsung-Wei Huang"(tsung-wei-huang)
    # https://github.com/taskflow/taskflow


    #REPO_USER_NAME  = input("Enter the name of the Git repository Owner: ")
    REPO_USER_NAME   = 'taskflow'
    #GITHUB_TOKEN    = input("Enter the GitHub Authentication Token: ")
    GITHUB_TOKEN     = ''
    #REPO_NAME       = input("Enter the name of the Git repository: ")
    REPO_NAME        = 'taskflow in:name'

    repoInitStatus, repo, pr_list = validate_GitRepoInfo(GITHUB_TOKEN, REPO_USER_NAME, REPO_NAME )
    
    if repoInitStatus == 'SUCCESS':
        PULL_REQUEST_NUMBER = input("Enter PR Number for code review : ")
        
        print("Starting code review...")
        files = get_pull_request_files(REPO_USER_NAME, REPO_NAME, PULL_REQUEST_NUMBER, GITHUB_TOKEN)

        #comments = analyze_changes_with_code_llama(files)
        comments = codeReview_ollama_wrapper(files)
        
        # post_review_comments(REPO_USER_NAME, REPO_NAME, PULL_REQUEST_NUMBER, comments, GITHUB_TOKEN)
        #post_review_comments(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PR_NUMBER,COMMENT,FILE_PATH,LINE_NUMBER):
    else:
        PrReviewStatus = 'FALSE'

# Start code review
InitiateCodeReview()