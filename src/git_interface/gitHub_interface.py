# gitHub_interface.py
import requests
from git import Repo
from github import Github

def validate_GitRepoInfo(GITHUB_TOKEN, REPO_USER_NAME, REPO_NAME ):
    
    repoInitStatus = 'FAILURE'
    gitTokenStatus = 'FAILURE'
    repo = ''
    pr_list = ''
        
    gitTokenStatus = validateGitToken(GITHUB_TOKEN)
    print("Git Token Status",gitTokenStatus)

    if (gitTokenStatus == 'SUCCESS'):
      
        gitRepoStatus, repo = validateGitRepo(GITHUB_TOKEN, REPO_NAME, REPO_USER_NAME)
        print("Git Repo Status",gitRepoStatus)

        if (gitRepoStatus == 'SUCCESS'):
            prListStatus, pr_list = getPullRequestList(GITHUB_TOKEN,REPO_USER_NAME,REPO_NAME)
        
            if(prListStatus == 'SUCCESS'):
                print("Code Review Can be initiated from the above PR lists")
                repoInitStatus = 'SUCCESS'
            else:
                print("No active pull request found")
        else:
            print("Check for git Rate Limit")
            #getRateLimit(GITHUB_TOKEN)
    
    return repoInitStatus, repo, pr_list

# Function to review the file line by line
def review_PullRequest(GITHUB_TOKEN, REPO_OWNER, REPO_NAME,PR_NUMBER):
    PrReviewStatus = 'FAILURE'
    # GitHub API URL for listing files in a pull request
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/files'

    # Headers for authentication
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the GET request to list files in the pull request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        for file in files:
            print("Review Started :", file)
            print(f"File: {file['filename']}, Status: {file['status']}")
            file_path = file['filename']
            file_url = f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{file_path}'
            response = requests.get(file_url)
            if response.status_code == 200:
                file_lines =  response.text.splitlines()
            else:
                print(f'Failed to get file content for {file_path}: {response.status_code}')
                return PrReviewStatus
                        
            comments = review_file(file_path, file_lines)
            for line_comment in enumerate(comments):
                COMMENT = line_comment['body']
                if COMMENT != 'NULL':
                    LINE_NUMBER = line_comment['position']
                    post_review_comments(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PR_NUMBER, COMMENT, file_path, LINE_NUMBER)
    else:
        print(f'Failed to get files: {response.status_code}')
        print(response.json())
        return PrReviewStatus

    PrReviewStatus = 'SUCCESS'
    return PrReviewStatus

# Function to review the file line by line
def review_file(FILE_PATH, file_lines):
    comments = []
    for i, line in enumerate(file_lines):
        # Example review logic
        if 'TODO' in line:
            comments.append({
                'path': FILE_PATH,
                'position': i + 1,
                'body': 'NULL'
            })
    return comments

def validateGitToken(GITHUB_TOKEN):
    gitTokenStatus = 'FAILURE'
    url = 'https://api.github.com/user'

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Token is valid.")
        #print(response.json())
        gitTokenStatus = 'SUCCESS'
    else:
        print(f"Error: {response.status_code}")
        #print(response.json())
        gitTokenStatus = 'FAILURE'

    return gitTokenStatus

def validateGitRepo(GITHUB_TOKEN, REPO_NAME, REPO_USER_NAME):
    gitRepoStatus = 'FAILURE'
    repo = ''
    url = f'https://api.github.com/search/repositories?q={REPO_NAME}'

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        substring_to_remove = ' in:name'
        CHECK_REPO_NAME = REPO_NAME.replace(substring_to_remove, '')
        print("Cheching for Repository ",CHECK_REPO_NAME)
        if 'items' in data:
            for currentRepoInList in data['items']:
                #print(currentRepoInList['name'])
                if(currentRepoInList['name'] == CHECK_REPO_NAME):
                    REPO_OWNER = currentRepoInList['owner']['login']
                    #print('Repo Owner : ', REPO_OWNER)
                    if(REPO_OWNER == REPO_USER_NAME):
                        gitRepoStatus = 'SUCCESS'
                        repo = currentRepoInList
                        return gitRepoStatus, repo
            print("No repositories found matching to the repository name")
            return gitRepoStatus, repo
        else:
            print("No repositories found")
    return gitRepoStatus, repo

def getRateLimit(GITHUB_TOKEN):
    headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
    }
    rate_limit_url = 'https://api.github.com/rate_limit'
    rate_limit_response = requests.get(rate_limit_url, headers=headers)
    print(rate_limit_response.json())

def getPullRequestList(GITHUB_TOKEN,REPO_OWNER,REPO_NAME):
    prListStatus = 'FAILURE'
    prList =''
    substring_to_remove = ' in:name'
    REPO_NAME = REPO_NAME.replace(substring_to_remove, '')
    # GitHub API URL for listing pull requests
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls'

    # Headers for authentication
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the GET request to list pull requests
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()
        pr_list = [f"PR #{pr['number']}: {pr['title']} by {pr['user']['login']}" for pr in pull_requests]
        for pr in pull_requests:
            print(f"PR #{pr['number']}: {pr['title']} by {pr['user']['login']}")
            PR_NUMBER = pr['number']
            #check_reviewComments(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PR_NUMBER)
        prListStatus = 'SUCCESS'
    else:
        print(f'Failed to get pull requests: {response.status_code}')
        print(response.json())
    
    return prListStatus, pr_list

def get_pull_request_files(owner, repo, pull_request_number, token):
    substring_to_remove = ' in:name'
    repo = repo.replace(substring_to_remove, '')

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}/files'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("\n Existing Review comments for the submitted PR \n ", pull_request_number)
        check_reviewComments(token, owner, repo, pull_request_number)
        return response.json()
    else:
        print(f'Failed to fetch files: {response.status_code}')
        return []

def post_review_comments(owner, repo, pull_request_number, comments, token):
    substring_to_remove = ' in:name'
    repo = repo.replace(substring_to_remove, '')

    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_request_number}/reviews'
    headers = {'Authorization': f'token {token}', 'Content-Type': 'application/json'}
    for comment in comments:
        print("Comments by AI Genie : ",comment)
        data = {
            "body": comment,
            "event": "COMMENT"
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f'Successfully posted comment: {comment}')
        else:
            print(f'Failed to post comment: {response.status_code} \n')

# Post review comments to GitHub
def post_file_review_comments(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PR_NUMBER,COMMENT,FILE_PATH,LINE_NUMBER):
    # GitHub API URL for creating a review comment
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/comments'

    # Headers for authentication
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Data for the review comment
    data = {
        'body': COMMENT,
        'path': FILE_PATH,
        'position': LINE_NUMBER
    }

    # Make the POST request to create the review comment
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print('Comment added successfully!')
    else:
        print(f'Failed to add comment: {response.status_code} \n')
        print(response.json())

def check_reviewComments(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PR_NUMBER):

    substring_to_remove = ' in:name'
    REPO_NAME = REPO_NAME.replace(substring_to_remove, '')
        
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/comments'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        comments = response.json()
        if comments:
            for comment in comments:
                print(f"Comment by {comment['user']['login']}: {comment['body']}")
        else:
            print("No review comments found.")
    else:
        print(f"Failed to fetch comments: {response.status_code}")