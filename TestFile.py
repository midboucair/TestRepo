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

    for f in files:
        filename = f.get("filename")
        status = f.get("status")
        additions = f.get("additions")
        deletions = f.get("deletions")
        print("\n" + "="*70)
        print(f"Fichier : {filename}")
        print(f"Statut  : {status} | +{additions} / -{deletions}")

        patch = f.get("patch")
        if not patch:
            print("(Pas de patch disponible — fichier binaire ou trop volumineux)")
            continue

        # Extraire les lignes ajoutées (+) et supprimées (-) dans le patch unifié
        added_lines = []
        removed_lines = []
        for line in patch.splitlines():
            # ignorer les en-têtes de hunk @@ ... @@
            if line.startswith('@@'):
                continue
            if line.startswith('+'):
                added_lines.append(line[1:])  # enlever le signe '+'
            elif line.startswith('-'):
                removed_lines.append(line[1:])  # enlever le signe '-'

        print("— Lignes supprimées (–) —")
        if removed_lines:
            for l in removed_lines[:20]:
                print(f"- {l}")
            if len(removed_lines) > 20:
                print(f"... (+{len(removed_lines)-20} autres)")
        else:
            print("(aucune)")

        print("— Lignes ajoutées (+) —")
        if added_lines:
            for l in added_lines[:20]:
                print(f"+ {l}")
            if len(added_lines) > 20:
                print(f"... (+{len(added_lines)-20} autres)")
        else:
            print("(aucune)")


if __name__ == "__main__":
    # 🔁 Remplace par tes valeurs (celles de ton JSON qui marche)
    owner = "midboucair"
    repo = "TestRepo"
    before = "c01a54974032077fe9f640136b4f3cf80200fd06"
    after  = "3e04b8b5e758d4f4f9aeeaf9298c56ff9babe4b7"

    # Si repo public -> token = None. Si privé -> mets ton token ici :
    token = None  # ex: "ghp_XXXXXXXXXXXXXXXXXXXXXXXX"

    test_compare_api(owner, repo, before, after, token)
