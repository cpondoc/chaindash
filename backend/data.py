'''
Grab developer data using Electric Capital Ecosystem Repository
'''
import toml
import sqlite3
import requests
from github import Github

# CHANGE TO COLLECT DATA ON NEW CHAINS
chains = ["polygon"]
database_file = "db/sample_data.db"

'''
Function to get all of chain data from Github
'''
def get_chain_data(chain, con, cur):
    # Make request and get ecosystem data
    print("Processing " + chain + " ecosystem:")
    toml_url = "https://raw.githubusercontent.com/electric-capital/crypto-ecosystems/master/data/ecosystems/" + chain[0] + "/" + chain + ".toml"
    r = requests.get(toml_url)
    eco_toml = toml.loads(r.text)

    # Track total repos, forks, etc.
    total_repos = 0
    total_forks = 0
    total_commits = 0
    total_stars = 0
    contribs = set()

    # Github token using config file
    config = toml.load("config.toml")
    g = Github(config[chain])
    counter = 0
    # Iterate through each repository
    for repo in eco_toml['repo']:

        # Try pulling data, and check if repo exists/is public
        counter += 1
        repo_name = repo['url'].replace("https://github.com/", "")
        print("Parsing data for repository: " + repo_name)
        print("Repository Number: " + str(counter))
        try:
            # Github token using config file
            repo_data = g.get_repo(repo_name)
        except:
            print("Couldn't get data on repository.")
        else:
            # Grab all data about specific repository
            forks = repo_data.forks
            commits = 0
            stars = repo_data.stargazers_count
            contributors = repo_data.get_contributors().totalCount

            # Update data
            total_repos += 1
            total_forks += forks
            total_stars +=  stars

            # Try accessing commits
            try:
                commits = repo_data.get_commits().totalCount
            except:
                print("Repository is empty.")
            else:
                total_commits += commits
            
            # May count bots, but get all unique contributors
            for contrib in repo_data.get_contributors():
                contribs.add(contrib.login)

            # Make update to SQL table
            cur.execute("INSERT INTO repositories VALUES ('" + repo_name + "', '" + chain + "', " + str(commits) + ", " + str(stars) + ", " + str(contributors) + ", " + str(forks) + ")")
            con.commit()
    
    # Commit statistics to each ecosystem
    cur.execute("INSERT INTO chains VALUES ('" + chain + "', " + str(total_commits) + ", " + str(total_stars) + ", " + str(len(contribs)) + ", " + str(total_forks) + ")")
    con.commit()

'''
Connects to database and runs program on each chain as specified
'''
if __name__ == "__main__":
    con = sqlite3.connect(database_file)
    cur = con.cursor()
    for chain in chains:
        get_chain_data(chain, con, cur)