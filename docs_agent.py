import os
import json
import requests
import sys
import re  # Import the regex module

def retrieve_and_store_docs(url: str):
    """Fetches documentation and repository information from a given GitHub URL and stores it."""
    base_docs_path = '/home/juan/crypto_payment_system/docs'
    github_api_base_url = 'https://api.github.com/repos'
     # Ensure the base 'docs' folder exists
    os.makedirs(base_docs_path, exist_ok=True)

    try:
        # Use regex to extract owner and repo name from the URL
        match = re.search(r"github\.com/([^/]+)/([^/]+)(?:\.git|/|$)", url)
        if not match:
            print("Invalid GitHub URL.")
            return

        owner, repo = match.groups()

        # Fetch the repository information
        repo_info_response = requests.get(f"{github_api_base_url}/{owner}/{repo}")
        repo_info_response.raise_for_status()
        repo_info = repo_info_response.json()

        # Optionally, print or store repo_info
        print(f"Repository Name: {repo_info['name']}")
        print(f"Description: {repo_info['description']}")
        print(f"Stars: {repo_info['stargazers_count']}")

        # Fetch the content from the URL (for documentation, if needed)
        response = requests.get(url)
        response.raise_for_status()

        # Create a unique path for the program's documentation
        unique_path = os.path.join(base_docs_path, repo)
        os.makedirs(unique_path, exist_ok=True)

        # Define the path to save the file, now within the unique folder
        filepath = os.path.join(unique_path, repo)

        # Write the repository information to a file in the unique folder
        with open(filepath, 'w') as file:
            json.dump(repo_info, file)
        print(f"Repository information saved to {filepath}")
    except requests.RequestException as e:
        print(f"Error fetching documentation or repository information: {e}")

def view_docs(repo: str):
    """Displays all the documentation for a given repository in a structured format."""
    base_docs_path = '/home/juan/crypto_payment_system/docs'
    doc_path = os.path.join(base_docs_path, repo, repo)

    try:
        with open(doc_path, 'r') as file:
            repo_info = json.load(file)

            print(f"Documentation for {repo}:")
            for key, value in repo_info.items():
                print(f"{key}: {value}")
    except FileNotFoundError:
        print(f"No documentation found for {repo}.")
    except json.JSONDecodeError:
        print(f"Error reading the documentation for {repo}. The file may be corrupted or not in the expected format.")

def list_current_repos():
    """Lists all repositories for which documentation is available."""
    base_docs_path = '/home/juan/crypto_payment_system/docs'

    try:
        # List directories only
        repos = [name for name in os.listdir(base_docs_path) if os.path.isdir(os.path.join(base_docs_path, name))]
        if repos:
            print("Available documentation for the following repositories:")
            for repo in repos:
                print(f"- {repo}")
        else:
            print("No documentation available.")
    except FileNotFoundError:
        print(f"The base documentation path {base_docs_path} does not exist.")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "view":
        repo = sys.argv[2]
        view_docs(repo)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "list":
            list_current_repos()
        else:
            url = sys.argv[1]
            retrieve_and_store_docs(url)
    else:
        print("Usage: python docs_agent.py <GitHub URL> or python docs_agent.py view <Repository Name> or python docs_agent.py list")