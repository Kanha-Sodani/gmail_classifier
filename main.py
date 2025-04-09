import re
import os
import joblib
import logging
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\d+', '', text)  # Remove digits
    return text

def create_combined_message(subject, snippet):
    combined = (subject or '') + ' ' + (snippet or '')
    return preprocess_text(combined)

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

def get_label_id(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    label = service.users().labels().create(userId='me', body={"name": label_name}).execute()
    return label['id']

def classify_emails():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Load model and vectorizer
    loaded = joblib.load('model.joblib')
    model = loaded['model']
    vectorizer = loaded['vectorizer']
    label_id = get_label_id(service, 'Banking')

    results = service.users().messages().list(userId='me', maxResults=200).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        snippet = msg_data.get('snippet', '')

        combined_message = create_combined_message(subject, snippet)
        transformed = vectorizer.transform([combined_message])
        prediction = model.predict(transformed)[0]

        if prediction == 1:
            service.users().messages().modify(
                userId='me', id=msg['id'], body={'addLabelIds': [label_id]}
            ).execute()

    logging.info("Classification complete.")

if __name__ == '__main__':
    classify_emails()
