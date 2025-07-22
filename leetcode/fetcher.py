import os
import requests
from dotenv import load_dotenv

load_dotenv()

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")
USERNAME = os.getenv("USERNAME")

headers = {
    "x-csrftoken": LEETCODE_CSRF_TOKEN,
    "cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={LEETCODE_CSRF_TOKEN}",
    "referer": "https://leetcode.com",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
session.headers.update(headers)

def get_accepted_submissions(limit=1000):

    test_res = session.get("https://leetcode.com/api/problems/all/")
    print(test_res.status_code)
    print(test_res.text) 

    print(f"Fetching up to {limit} accepted submissions...")
    submissions = []
    offset = 0
    has_more = True

    while has_more and len(submissions) < limit:
        query = {
            "operationName": "Submissions",
            "variables": {
                "offset": offset,
                "limit": 20,
                "questionSlug": None
            },
            "query": """
            query Submissions($offset: Int!, $limit: Int!, $questionSlug: String) {
            submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
                hasNext
                submissions {
                id
                title
                titleSlug
                statusDisplay
                lang
                timestamp
                }
            }
            }
            """
        }


        res = session.post("https://leetcode.com/graphql/", json=query)

        try:
            data = res.json()
            if "errors" in data:
                print("[❌] GraphQL error:", data["errors"])
                break
            subs = data["data"]["submissionList"]["submissions"]
            accepted_subs = [s for s in subs if s["statusDisplay"] == "Accepted"]
            submissions.extend(accepted_subs)
        except Exception as e:
            print("[❌] Failed to parse response:")
            print(res.text)  # Show the full HTML or error response
            print("Exception:", e)
            break

        offset += 20

    return submissions[:limit]
