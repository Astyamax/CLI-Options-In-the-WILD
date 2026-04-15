import requests
from git import Repo
from datetime import datetime
import subprocess

def find_main_repo(name):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": name,
        "per_page": 10
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    items = r.json()["items"]

    if not items:
        return None

    name_lower = name.lower()

    # 1. Exact repo name match
    for repo in items:
        if repo["name"].lower() == name_lower:
            return repo["clone_url"]

    # 2. Exact full_name match (org/name)
    for repo in items:
        if repo["full_name"].lower().endswith("/" + name_lower):
            return repo["clone_url"]

    # 3. Fallback: most stars
    items.sort(key=lambda r: r["stargazers_count"], reverse=True)
    return items[0]["clone_url"]


prg = input("program : ")
repo_url = find_main_repo(prg)

print(repo_url)


local_path = "downloads/tmp/"
subprocess.run(["rm", "-rf", local_path])

# Clone repo (or open if already cloned)
repo = Repo.clone_from(repo_url, local_path)

# Get tags (versions)
for tag in repo.tags:
    try:
        commit = tag.commit  # may fail
        date = datetime.fromtimestamp(commit.committed_date)
        print(f"{tag.name} - {date}")
    except ValueError:
        # Skip tags that don't point to commits
        continue