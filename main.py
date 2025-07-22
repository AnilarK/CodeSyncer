from leetcode.fetcher import get_accepted_submissions

if __name__ == "__main__":
    submissions = get_accepted_submissions(50)
    for sub in submissions[:5]:
        print(f"{sub['title']} | {sub['lang']} | {sub['timestamp']}")