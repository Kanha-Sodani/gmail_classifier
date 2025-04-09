from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def set_watch(service):
    request_body = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/gmail-classifier-454221/topics/gmail-notifications'
    }
    response = service.users().watch(userId='me', body=request_body).execute()
    print("✅ Gmail watch set:", response)

if __name__ == '__main__':
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    set_watch(service)
