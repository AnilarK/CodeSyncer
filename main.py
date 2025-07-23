from leetcode.fetcher import get_accepted_submissions
from leetcode.fetcher import get_submission_code
from github.github import upload_to_github
from db.mongo import get_mongo_client

if __name__ == "__main__":

    submissions = get_accepted_submissions()
    submissions.reverse()
    timestamp=0
    for sub in submissions:
        code = get_submission_code(sub['id'])
        sub['code'] = code["code"]
        upload_to_github(sub)
        timestamp = max(timestamp,  int(sub["timestamp"]))
    
    db = get_mongo_client()
    collection = db["Leetcode"]
    doc = collection.find_one(sort=[("timestamp", -1)])
    result = collection.find_one_and_update(
        { "_id": doc["_id"]},
        { "$set": { "timestamp": timestamp } },
        return_document=True
    )




    