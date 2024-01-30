import json
import requests
import csv
from colorama import Fore, Back, Style

import os

# check if data folder exists
if not os.path.exists("data"):
 os.makedirs("data")

# programming languages and respective types
programming_languages = {
    "Python": [".py", ".pyw", ".pyc", ".pyd", ".pyo", ".py3"],
    "Java": [".java", ".jar", ".jmod"],
    "C": [".c"],
    "C++": [".cpp", ".cxx", ".cc"],
    "C#": [".cs", ".csx", ".cake"],
    "JavaScript": [".js", ".mjs", ".cjs"],
    "TypeScript": [".ts", ".tsx"],
    "PHP": [".php", ".phtml", ".php3", ".php4", ".php5", ".phps"],
    "Ruby": [".rb", ".erb"],
    "Swift": [".swift"],
    "Kotlin": [".kt", ".kts", ".ktm"],
    "Go": [".go"],
    "Rust": [".rs", ".rlib"],
    "Perl": [".pl", ".pm", ".t", ".pod"],
    "Scala": [".scala", ".sc"],
    "Lua": [".lua"],
    "Haskell": [".hs", ".lhs"],
    "Objective-C": [".m", ".mm"],
    "Dart": [".dart"],
    "Groovy": [".groovy", ".gvy", ".gy", ".gsh"],
    "Shell": [".sh", ".bash", ".zsh"],
    "SQL": [".sql"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "XML": [".xml"],
    "JSON": [".json"],
    "YAML": [".yaml", ".yml"],
    "Markdown": [".md", ".markdown"]
}

# Check if file is source file
def is_source_file(filename, languages):
    file_extension = os.path.splitext(filename)[1]
    print(file_extension)
    for lang in languages:
        if file_extension in programming_languages.get(lang, []):
            return True
    return False

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

# @repo, Github repo
# @lstTokens, GitHub authentication tokens
def get_repo_languages(repo, lsttokens):
    languages_url = 'https://api.github.com/repos/{repo}/languages'
    languages_data, _ = github_auth(languages_url, lsttokens, 0)
    print(languages_data)
    return list(languages_data.keys()) if languages_data else []

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    
    # get languages in repo
    languages = get_repo_languages(repo, lsttokens)
    print("Languages in repo:")
    
    print(Fore.RED)
    print(languages)
    print(Style.RESET_ALL)
    
    print(Fore.GREEN + "Source files green: ")
    print(Style.RESET_ALL)

    if not languages:
        print("No languages found for the repository.")
        return
    
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)
            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break

            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:

                    filename = filenameObj['filename']
                    print(filename)

                    if is_source_file(filename, languages):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(Fore.GREEN + filename)
                        print(Style.RESET_ALL)


            ipage += 1
    except Exception as e:
        print(f"Exception: {e}")
        exit(0)


# GitHub repo
repo = 'scottyab/rootbeer'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [   "aaaaaaa"
                ]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()

print(Fore.BLUE)
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
