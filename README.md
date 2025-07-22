# 🚀 CodeSyncer

**CodeSyncer** is an automation tool that fetches your accepted solutions from coding platforms like **LeetCode** and **GeeksforGeeks**, and **automatically pushes them to a structured GitHub repository**.

Whether you're a competitive programmer, job aspirant, or someone who wants a clean public record of your problem-solving journey — CodeSyncer has your back!

---

## ✨ Features

- 🔄 **Auto-fetch** accepted submissions from LeetCode (GFG support coming soon)
- 🚀 **Auto-push** solutions to GitHub with structured file/folder naming
- 🔥 **Streak tracking** across accounts
- 👥 **Multi-user support** (handle multiple LeetCode/GFG profiles)
- 🧱 Modular design — easily extend to Codeforces, AtCoder, etc.
- ⏱️ Schedule it using `cron` or `Task Scheduler` to run automatically
- 📊 (Upcoming) Submission insights and dashboard

---

## 🛠️ Tech Stack

| Tool/Library       | Purpose                              |
|--------------------|--------------------------------------|
| Python             | Core logic scripting                 |
| Requests / GraphQL | API access to LeetCode               |
| GitPython / CLI    | GitHub integration                   |
| BeautifulSoup      | Parsing HTML (for GFG)               |
| `dotenv`           | Environment variable management      |
| Logging            | Debug and tracking                   |

---

## 📁 Project Structure

```bash
CodeSyncer/
├── leetcode/
│   ├── fetcher.py         # Fetch LeetCode submissions
│   └── parser.py          # Clean and format code
├── gfg/
│   ├── fetcher.py         # (Coming soon)
│   └── parser.py
├── github/
│   └── sync.py            # Push to GitHub repo
├── utils/
│   ├── config.py          # Load .env and settings
│   └── logger.py          # Custom logging
├── main.py                # Entry point
├── .env                   # LeetCode session, GitHub token, etc.
└── README.md
