import httpx

# Your GitHub personal access token
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
# Repositories to keep active and not archive or set to private
repos_to_keep_active = ['repo1', 'repo2']

headers = {
	'Authorization': f'token {GITHUB_TOKEN}',
	'Accept': 'application/vnd.github.v3+json',
}

def get_repos():
	"""Fetch all repositories for the authenticated user."""
	url = 'https://api.github.com/user/repos'
	response = httpx.get(url, headers=headers)
	response.raise_for_status()
	return response.json()

def update_repo_visibility(repo_name, visibility='private'):
	"""Update a repository's visibility to private."""
	url = f'https://api.github.com/repos/{repo_name}'
	data = {'visibility': visibility}
	response = httpx.patch(url, headers=headers, json=data)
	response.raise_for_status()

def archive_repo(repo_name):
	"""Archive a repository."""
	url = f'https://api.github.com/repos/{repo_name}'
	data = {'archived': True}
	response = httpx.patch(url, headers=headers, json=data)
	response.raise_for_status()

def main():
	repos = get_repos()
	for repo in repos:
		repo_name = repo['full_name']
		if repo_name not in repos_to_keep_active:
			# Uncomment the next line to set repositories to private
			# update_repo_visibility(repo_name, 'private')
			# Uncomment the next line to archive repositories
			# archive_repo(repo_name)
			print(f'Updated {repo_name}')

if __name__ == '__main__':
	main()


