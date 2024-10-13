import os
import requests
import base64

repo_owner = "smaugue"
repo_name = "GameBot"
branch_name = "main"
token = "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"
ignore_files = ["updater.py"]

local_folder = os.path.dirname(os.path.abspath(__file__))

def get_version():
    try:
        with open("Version", encoding='utf-8') as data:
            lines = data.readlines()
            for line in lines:
                if "VERSION" in line:
                    v, u, p = line.split("=")[1].strip().replace('"', '').replace("'", "").split(".")
                    return int(v), int(u), int(p)
    except FileNotFoundError:
        print("Le fichier 'Version' est introuvable.")
        return None

version_tuple = get_version()
if version_tuple:
    v, u, p = version_tuple
    BOT_VERSION = f"{v}.{u}.{p}"

class Version:
    LATEST_VERSION = ""

    @staticmethod
    def get_github_data(file_path):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch_name}"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json().get('content', '')
            if content:
                decoded_content = base64.b64decode(content).decode('utf-8')
                return decoded_content
        else:
            print(f"Erreur lors de la récupération des données depuis GitHub : {response.status_code}")
            return None

    @staticmethod
    def get_github_version():
        decoded_content = Version.get_github_data("Version")
        if decoded_content:
            for line in decoded_content.split("\n"):
                if "VERSION" in line:
                    v, u, p = line.split("=")[1].strip().replace('"', '').replace("'", "").split(".")
                    return int(v), int(u), int(p)
        return None

    @staticmethod
    def cmp():
        github_version = Version.get_github_version()
        if github_version:
            bv, bu, bp = github_version
            Version.LATEST_VERSION = f"{bv}.{bu}.{bp}"
            if v < bv or (v == bv and u < bu) or (v == bv and u == bu and p < bp):
                return "older"
            if v > bv or (v == bv and u > bu) or (v == bv and u == bu and p > bp):
                return "newer"
            return "up_to_date"
        else:
            print("Impossible de récupérer la version GitHub.")
            return None

    @staticmethod
    def download_file_from_github(file_path):
        decoded_content = Version.get_github_data(file_path)
        if decoded_content:
            local_file_path = os.path.join(local_folder, file_path)
            with open(local_file_path, 'w', encoding='utf-8') as local_file:
                local_file.write(decoded_content)
            print(f"Fichier {file_path} mis à jour.")
        else:
            print(f"Impossible de récupérer le contenu du fichier {file_path}.")

    @staticmethod
    def update_files():
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents?ref={branch_name}"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            for file_info in files:
                file_name = file_info['name']
                if file_name not in ignore_files:
                    Version.download_file_from_github(file_name)
        else:
            print(f"Erreur lors de la récupération des fichiers depuis GitHub : {response.status_code}")

    @staticmethod
    def update_if_needed():
        result = Version.cmp()
        os.system("cls||clear")
        if result == "older":
            print(f"Version locale ({BOT_VERSION}) plus ancienne que la version GitHub ({Version.LATEST_VERSION}). Mise à jour en cours...")
            Version.update_files()
            print("Mise à jour réussie.")
        elif result == "newer":
            print(f"\nATTENTION : La version locale ({BOT_VERSION}) est plus récente que la version sur GitHub ({Version.LATEST_VERSION}).\n")
            print("Aucune mise à jour effectuée.")
        elif result == "up_to_date":
            print("La version locale est à jour.")
        else:
            print("Aucune action effectuée en raison d'une erreur.")

if __name__ == "__main__":
    if version_tuple:
        Version.update_if_needed()
