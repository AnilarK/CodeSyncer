from dotenv import load_dotenv
import os

load_dotenv()

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("USERNAME")
HEADERS = {
    'cookie': f'LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={LEETCODE_CSRF_TOKEN}',
    'x-csrftoken': LEETCODE_CSRF_TOKEN,
    'Content-Type': 'application/json'
}
