import requests
import base64

repo_owner = "smaugue"
repo_name = "GameBot"
file_path = "Version"
token = "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"

def get_version():
    data = open("Version")
    lines = data.readlines()
    for line in lines:
        if "VERSION" in line:
            v, u, p = line.split("=")[1].strip().replace('"', '').replace("'", "").split(".")
            return int(v), int(u), int(p)

v,u,p = get_version()

BOT_VERSION = f"{v}.{u}.{p}"

class Version:

    LASTER_VERSION = ""

    def get_github_data():
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json().get('content', '')
            if content:
                decoded_content = base64.b64decode(content).decode('utf-8')
                return decoded_content
        else:
            response.raise_for_status()
        return None
    
    def get_github_patch():
        decoded_content = Version.get_github_data()
        date = "-/-/-"
        patch = "Non renseigné..."
        for line in decoded_content.split("\n"):
            if "DATE" in line:
                date = line.split("=")[1].strip().replace('"', '').replace("'", "")
            if "PATCH" in line:
                patch = line.split("=")[1].strip().replace('"', '').replace("'", "")
        return date, patch


    def get_github_version():
        decoded_content = Version.get_github_data()
        for line in decoded_content.split("\n"):
            if "VERSION" in line:
                v, u, p = line.split("=")[1].strip().replace('"', '').replace("'", "").split(".")
                return int(v), int(u), int(p)

    def cmp(version: str):
        bv, bu, bp = Version.get_github_version()
        Version.LASTER_VERSION = f"{bv}.{bu}.{bp}"
        if v < bv:
            return "o"
        if v == bv and u < bu:
            return "o"
        if v == bv and u == bu and p < bp:
            return "o"
        if v > bv:
            return "b"
        if v == bv and u > bu:
            return "b"
        if v == bv and u == bu and p > bp:
            return "b"
        return "j"
    
    def check():
        return Version.cmp(BOT_VERSION)
    
    def get_patch():
        return Version.get_github_patch()