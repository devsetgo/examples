import httpx
from dotenv import load_dotenv
import os
from pprint import pprint
# Load environment variables from .env file
load_dotenv()

# Your GitHub personal access token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
# Repositories to keep active and not archive or set to private
repos_to_keep_active = ['devsetgo/devsetgo_lib', 'devsetgo/dsg', 'devsetgo/devsetgo', 'devsetgo/examples','devsetgo/7oi']

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}


def get_repos():
    """Fetch all repositories for the authenticated user."""
    url = 'https://api.github.com/user/repos?type=all&per_page=100'
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def update_repo_visibility(repo_name, visibility='private'):
    """Update a repository's visibility."""
    # Ensure the repo_name is correctly specified with owner/repo format
    url = f'https://api.github.com/repos/{repo_name}'
    data = {f'visibility': visibility}
    try:
        response = httpx.patch(url, headers=headers, json=data)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response status code: {e.response.status_code}")
        print(f"Response body: {e.response.text}")
        # Additional logging or handling

def unarchive_repo(repo_name):
    """Unarchive a repository."""
    url = f'https://api.github.com/repos/{repo_name}'
    data = {'archived': False}
    response = httpx.patch(url, headers=headers, json=data)
    response.raise_for_status()

def archive_repo(repo_name):
    """Archive a repository."""
    # Directly use repo_name without adding 'devsetgo/'
    url = f'https://api.github.com/repos/{repo_name}'
    data = {'archived': True}
    response = httpx.patch(url, headers=headers, json=data)
    response.raise_for_status()



def main():
    repos = get_repos()  # Fetch the list of repositories
    for repo in repos:
        repo_name = repo['full_name']
        if repo_name not in repos_to_keep_active:
            # If the repo is archived but not private, unarchive it first
            if repo['archived'] and repo['visibility'] != 'private':
                try:
                    unarchive_repo(repo_name)  # Unarchive the repository
                    update_repo_visibility(repo_name, 'private')  # Make the repository private
                    archive_repo(repo_name)  # Archive the repository again
                    print(f"Unarchived, made private, and re-archived {repo_name}")
                except httpx.HTTPStatusError as e:
                    print(f"Failed to update {repo_name}: {e}")
            # If the repo is not archived, or it's not private
            elif not repo['archived'] or repo['visibility'] != 'private':
                if not repo['archived']:
                    try:
                        update_repo_visibility(repo_name, 'private')  # Make the repository private
                        archive_repo(repo_name)  # Archive the repository
                        print(f"Made private and archived {repo_name}")
                    except httpx.HTTPStatusError as e:
                        print(f"Failed to update {repo_name}: {e}")
                elif repo['visibility'] != 'private':
                    try:
                        update_repo_visibility(repo_name, 'private')  # Make the repository private
                        # No need to archive again since it's already archived
                        print(f"Made private {repo_name}")
                    except httpx.HTTPStatusError as e:
                        print(f"Failed to make {repo_name} private: {e}")
        else:
            print(f"Skipping {repo_name}, it's in the repos_to_keep_active list.")
        
        # print(f'Updated {repo_name} repo_private: {repo_vis} repo_archived: {repo_arch}')


if __name__ == '__main__':
    main()
