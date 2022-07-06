'''
Reading in ecosystem data
'''
import toml
import requests
from github import Github

# Github token using config file
config = toml.load("config.toml")
g = Github(config['token'])

# Getting ecosystem stats on a specific ecosystem
def get_ecosystem_stats(url):
    # Make request and get ecosystem data
    r = requests.get(url)
    eco_toml = toml.loads(r.text)

    # Track total repos, forks, etc.
    total_repos = 0
    total_forks = 0
    total_commits = 0
    contribs = set()

    # Iterate through each repository
    for repo in eco_toml['repo']:

        # Try pulling data, and check if repo exists/is public
        repo_name = repo['url'].replace("https://github.com/", "")
        print("Parsing data for repository: " + repo_name)
        try:
            repo_data = g.get_repo(repo_name)
        except:
            print("Couldn't get data on repository.")
        else:
            # Increase repos, forks, and commits
            total_repos += 1
            total_forks += repo_data.forks
            commits = 0
            try:
                commits = repo_data.get_commits().totalCount
            except:
                print("Repository is empty.")
            else:
                total_commits += commits
            
            # May count bots, but get all unique contributors
            for contrib in repo_data.get_contributors():
                contribs.add(contrib.login)
    return total_repos, total_forks, total_commits, len(contribs)


# Practice calling in Gitcoin toml file
if __name__ == "__main__":

    # Load in all chains
    chains_toml = toml.load("chains.toml")
    chains = chains_toml['chains']

    # Iterate through each chain and call function to get ecosystem stats
    for chain in chains:
        toml_url = "https://raw.githubusercontent.com/electric-capital/crypto-ecosystems/master/data/ecosystems/" + chain[0] + "/" + chain + ".toml"
        print("Get Ecosystem Stats for " + chain)
        repos, forks, commits, contribs = get_ecosystem_stats(toml_url)

        # Print statistics 
        print("Total Number of Repositories: " + str(repos))
        print("Total Number of Forks: " + str(forks))
        print("Total Number of Commits: " + str(commits))
        print("Total Number of Contributors: " + str(contribs))