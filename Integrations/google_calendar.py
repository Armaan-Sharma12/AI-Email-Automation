import datetime
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the token_calendar.pickle file.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
TOKEN_PATH = 'auth/token_calendar.pickle'
CREDS_PATH = 'auth/credentials.json'


def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def add_event_to_calendar(summary: str, description: str, date: str):
    service = get_calendar_service()

    # Convert string to datetime.date
    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print(f"❌ Invalid date format: {date}")
        return

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'date': parsed_date.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'date': (parsed_date + datetime.timedelta(days=1)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"📅 Calendar event created: {event_result.get('htmlLink')}")

