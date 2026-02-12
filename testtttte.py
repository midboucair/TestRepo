import requests
import re
from typing import Optional

def test_compare_api(owner: str, repo: str, before_sha: str, after_sha: str, token: Optional[str] = None):
    """
    Appelle la GitHub Compare API et affiche, pour chaque fichier, les lignes ajoutées/supprimées.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{before_sha}...{after_sha}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "impact-analyzer-mini"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(url, headers=headers, timeout=30)
    print(f"HTTP {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        return

    data = resp.json()
    print(f"status: {data.get('status')}, total_commits: {data.get('total_commits')}")
    files = data.get("files", [])
    if not files:
        print("Aucun fichier modifié.")
        return
