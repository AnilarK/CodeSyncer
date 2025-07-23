import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def upload_to_github(sub):
    title = sub["titleSlug"]
    code = sub["code"]
    lang = sub["lang"]
    
    url = f"https://leetcode.com/problems/{title}/"
    if lang == "cpp":
        code = f"// {url}\n\n{code}"
        ext = "cpp"
    elif lang == "python3" or lang == "python":
        code = f"# {url}\n\n{code}"
        ext = "py"
    elif lang == "java":
        code = f"// {url}\n\n{code}"
        ext = "java"
    else:
        ext = "txt"

    path = f"leetcode/dcc/{title}.{ext}"
    api_url = f"https://api.github.com/repos/AnilarK/code-store/contents/{path}"

    encoded_content = base64.b64encode(code.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    res = requests.get(api_url, headers=headers)
    if res.status_code == 200:
        sha = res.json()["sha"]
    else:
        sha = None

    payload = {
        "message": f"Add solution for : {title}",
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(api_url, headers=headers, json=payload)

    if r.status_code in [200, 201]:
        print(f"Uploaded {path}")
    else:
        print("Failed to upload:", r.status_code, r.text)
