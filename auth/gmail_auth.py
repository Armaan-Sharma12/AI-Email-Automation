import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Combined scopes for Gmail and Calendar
SCOPES = [
    'https://mail.google.com/',  # Full Gmail access
    'https://www.googleapis.com/auth/calendar.events'  # Calendar access
]


TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.pickle')
CREDS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')


def authenticate():
    creds = None

    # Load existing token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If not valid, refresh or go through OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_gmail_service():
    creds = authenticate()
    return build('gmail', 'v1', credentials=creds)


def get_calendar_service():
    creds = authenticate()
    return build('calendar', 'v3', credentials=creds)
