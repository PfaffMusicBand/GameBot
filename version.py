import requests

bot_version = "1.0.0"

repo_owner = "smaugue"
repo_name = "GameBot"
file_path = "Version"
token = "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"

class Version:

    def get_github_version(repo_owner: str, repo_name: str, file_path: str, token: str):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json().get('content', '')
            if content:
                # GitHub content is base64 encoded
                import base64
                decoded_content = base64.b64decode(content).decode('utf-8')
                # Assuming the version is on a line like: VERSION = "1.2.3"
                for line in decoded_content.split("\n"):
                    if "VERSION" in line:
                        print(line)
                        return int(line.split("=")[1].split("."))
        else:
            print(response.raise_for_status())
        return None

    def get_versions(version: str):
        v, u, p = version.split(".")
        return int(v), int(u), int(p)

    bv, bu, bp = get_github_version(repo_owner,repo_name, file_path, token)

    def cmp(version: str):
        v,u,p = Version.get_versions(version)
        if v < Version.bv:
            return "o"
        if v == Version.bv and u < Version.bu:
            return "o"
        if v == Version.bv and u == Version.bu and p < Version.bp:
            return "o"
        if v > Version.bv:
            return "b"
        if v == Version.bv and u > Version.bu:
            return "b"
        if v == Version.bv and u == Version.bu and p > Version.bp:
            return "b"
        return "j"
    
    def check():
        return Version.cmp(bot_version)