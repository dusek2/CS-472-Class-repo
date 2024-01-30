import json
import requests
import csv
from termcolor import colored


import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# get commits for specific @filename
def get_file_commits(repo, filename, lsttokens):
    commits = []
    ct = 0
    page = 1
    # loop until done with commit records
    while True:
        commits_url = 'https://api.github.com/repos/{repo}/commits?path={filename}&page={page}&per_page=100'
        jsonCommits, ct = github_auth(commits_url, lsttokens, ct)

        if not jsonCommits or len(jsonCommits) == 0:
            break
        # separate records
        for commit in jsonCommits:
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            commits.append((author, date))
            #print(author)
            #print(date)

        page += 1

    return commits

# get touches
def file_touches(repo, source_files, lsttokens):
    authors_touches = {}
    for file in source_files:
        print("Reading touches for file: " + file)
        commits = get_file_commits(repo, file, lsttokens)
        authors_touches[file] = commits
    return authors_touches

# GitHub repo
repo = 'scottyab/rootbeer'

print("Analyzing repo: " + repo)

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["aaaaaa"
                ]


def filenames_from_csv(csv_file_path, filename_col_index=0):
    source_filenames = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            if row:  # Check if row is not empty
                filename = row[filename_col_index]
                source_filenames.append(filename)
    return source_filenames


CSV = "data/file_rootbeer.csv"

print("Reading source filenames from csv: " + CSV)
source_files = filenames_from_csv(CSV)

print("Reading touches from github repo: " + repo)
file_touches = file_touches(repo, source_files, lstTokens)

print(colored('Reading done....\n','green'))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_dates_' + file + '.csv'
rows = ["Filename", "Author", "Date Touched"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, touches in file_touches.items():
    for author, date in touches:
        writer.writerow([filename, author, date])
