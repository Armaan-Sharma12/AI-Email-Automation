# 📬 AI Email Automation

Welcome to **AI Email Automation**, a Python-powered productivity tool that automates your Gmail inbox using AI! It classifies your emails with Cohere AI and takes smart actions like replying, drafting, deleting spam, creating calendar events, and sending Telegram alerts — all without you lifting a finger.

---

## 💡 Features

- ✅ Reads Gmail inbox via Gmail API
- 🧠 Uses Cohere AI for email classification
- ✉️ Auto-replies or saves drafts based on content
- 🗑️ Deletes junk/spam emails
- 📅 Adds events to Google Calendar if a deadline is found
- 📲 Sends Telegram alerts for important emails
- 💾 Saves metadata of each processed email to `emails.json`
- 🐳 Runs every 3 hours automatically via Docker + cron

---

## 📁 Project Structure

ai_email_automator/  
├── auth/  
│ ├── credentials.json # Google API credentials (ignored in git)  
│ ├── token.pickle # Gmail token (ignored)  
│ └── gmail_auth.py  
│  
├── classification/  
│ ├── cohere_classifier.py # Uses Cohere API  
│ └── json_utils.py # JSON cleanup  
│  
├── telegram_bot_module/  
│ └── telegram_bot.py # Sends alerts  
│  
├── automation/  
│ ├── email_handler.py # Main automation logic  
│ ├── gmail_reader.py # Fetch emails  
│ └── gmail_actions.py # Reply, draft, delete  
│  
├── Integrations/  
│ └── google_calendar.py # Calendar integration  
│  
├── .env # API keys and tokens (ignored)  
├── main.py # Runs email processor  
├── requirements.txt # Dependencies  
├── Dockerfile # Docker setup  
├── docker-compose.yml # Cron-enabled Docker runner  
└── README.md # You're reading it!  


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Armaan-Sharma12/AI-Email-Automation.git
cd AI-Email-Automation

```

### 2. Set Up Python Environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a .env File

```bash
COHERE_API_KEY=your-cohere-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

### 5. Add Google API Credentials

* Go to Google Cloud Console.

* Create OAuth credentials for Gmail & Calendar.

* Download credentials.json and place it in the auth/ folder.

## Docker Setup with Cron

This project runs automatically every 3 hours using cron inside a Docker container.  

### 1. Build and Run

```bash
docker-compose up --build -d
```

It will execute main.py every 3 hours inside the container using Alpine’s crond + shell script.  

## Files Ignored via .gitignore

Added the following to .gitignore to protect sensitive data and keep your repo clean:

```bash
.env
__pycache__/
*.pyc
.vscode/
*.log
*.DS_Store
venv/
auth/token_calendar.pickle
auth/token.pickle
auth/credentials.json
data/emails.json
```

 These files will stay safely on your machine and won’t be pushed to GitHub.  

 ## Contribute
 
 Want to help make this tool better? Awesome!  
Feel free to fork the repo, suggest ideas, fix bugs, or add new features.  

```bash
git checkout -b your-feature-branch
git commit -m "Add something cool"
git push origin your-feature-branch
```

Send a pull request and let’s make email management smarter together.   

 ## Author

 Armaan Sharma  
B.Tech CSE @ Amity University 
https://github.com/Armaan-Sharma12

Blog Post: [How I built this AI Email Assistant](https://dev.to/armaansharma12/automating-my-inbox-with-ai-a-python-email-assistant-using-cohere-gmail-api-and-telegram-alerts-k15)



 
