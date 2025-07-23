import os
import requests
from dotenv import load_dotenv
from db.mongo import get_mongo_client
import time

load_dotenv()
db = get_mongo_client()
collection = db["Leetcode"]


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

def get_accepted_submissions():
    doc = collection.find_one(sort=[("timestamp", -1)])
    last_cron_at = int(doc["timestamp"])
    # last_cron_at = int(time.time()) 

    print(f"Fetching accepted submissions after {last_cron_at}...")
    submissions = []
    offset = 0
    has_more = True

    while has_more :
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
                print("GraphQL error:", data["errors"])
                break

            subs = data["data"]["submissionList"]["submissions"]
            for sub in subs:
                submission_time = int(sub["timestamp"])

                if submission_time < last_cron_at:
                    has_more = False
                    break

                # print(submission_time, sub["title"])

                if sub["statusDisplay"] == "Accepted":
                    submissions.append(sub)
            
        except Exception as e:
            print("Failed to parse response:")
            print(res.text)
            print("Exception:", e)
            break

        offset += 20

    return submissions

def get_submission_code(submission_id):
    query = {
        "operationName": "submissionDetails",
        "variables": {
            "submissionId": int(submission_id)
        },
        "query": """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                code
                runtime
                memory
                lang {
                    name
                }
                timestamp
                question {
                    title
                    titleSlug
                }
            }
        }
        """
    }

    res = session.post("https://leetcode.com/graphql/", json=query)
    try:
        data = res.json()
        code_data = data["data"]["submissionDetails"]
        return code_data
    except Exception as e:
        print("Error fetching submission code:", e)
        print("Raw response:", res.text)
        return None


