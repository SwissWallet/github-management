from github import Github
import os

ORG_NAME = 'SwissWallet'
TOKEN = os.getenv('GITHUB_TOKEN')
TEMPLATE_FILE_PATH = os.path.abspath('./templates/PULL_REQUEST_TEMPLATE.md')

def read_template_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def update_pr_template(repo, template_content):
    
    try:
        
        contents = repo.get_contents('.github/PULL_REQUEST_TEMPLATE.md')
        sha = contents.sha
        repo.update_file(contents.path, "\nUpdating pull request template...", template_content, sha)
        print(f'PR template updated in {repo.full_name}.')
    except Exception as e:
    
        if "404" in str(e):
            repo.create_file('.github/PULL_REQUEST_TEMPLATE.md', "\nCreating pull request template...", template_content)
            print(f'PR template created in {repo.full_name}.')
        else:
            print(f'Update error in {repo.full_name}: {e}')

def main():
    
    g = Github(TOKEN)
    
    org = g.get_organization(ORG_NAME)

    template_content = read_template_file(TEMPLATE_FILE_PATH)
    
    for repo in org.get_repos():
        print(f'Updating template in {repo.full_name}...')
        update_pr_template(repo, template_content)

if __name__ == '__main__':
    main()