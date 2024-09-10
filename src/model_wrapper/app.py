from flask import Flask, jsonify, request
import os
import sys


prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model_interface'))
sys.path.insert(0, prompt_path)
prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'git_interface'))
sys.path.insert(0, prompt_path)

from ollama_interface import codeReview_ollama_wrapper
from gitHub_interface import validate_GitRepoInfo, get_pull_request_files, post_review_comments

app = Flask(__name__)

@app.route('/api/greet', methods=['GET'])
def greet():
    return jsonify({'message': 'Hello, World!'})
@app.route('/api/data', methods=['POST'])
def data():
    content = request.json
    return jsonify({'received': content})

@app.route('/api/code_review', methods=['POST'])
def initiate_code_review():
    data = request.json
    REPO_USER_NAME = data.get('repo_user_name', 'taskflow')
    GITHUB_TOKEN = data.get('github_token')
    REPO_NAME = data.get('repo_name', 'taskflow')
    PULL_REQUEST_NUMBER = data.get('pull_request_number')

    if not GITHUB_TOKEN:
        return jsonify({'error': 'GitHub token is required'}), 400

    repoInitStatus, repo, pr_list = validate_GitRepoInfo(GITHUB_TOKEN, REPO_USER_NAME, REPO_NAME)
    
    if repoInitStatus == 'SUCCESS':
        files = get_pull_request_files(REPO_USER_NAME, REPO_NAME, PULL_REQUEST_NUMBER, GITHUB_TOKEN)
        comments = codeReview_ollama_wrapper(files)
        post_review_comments(REPO_USER_NAME, REPO_NAME, PULL_REQUEST_NUMBER, comments, GITHUB_TOKEN)
        return jsonify({'status': 'success', 'comments': comments}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Failed to initialize repository'}), 400

if __name__ == '__main__':
    app.run(debug=True)
