# Gmail Classifier

This project is a real-time Gmail classifier that detects and filters banking-related emails using machine learning, the Gmail API, and Google Cloud Pub/Sub.

## Features

- Reads and processes Gmail inbox data securely
- Labels and classifies banking-related emails using a trained Naive Bayes model
- Uses Google Cloud Pub/Sub to monitor new email activity in real time
- Automatically classifies incoming emails when they arrive
- Modular structure for training, classification, and event listening

## Tech Stack

- Python
- Gmail API
- Google Cloud Pub/Sub
- Scikit-learn (Naive Bayes)
- Joblib
- OAuth2 / Service Accounts

## How It Works

1. **Data Collection**: Gmail API is used to fetch email metadata.
2. **Labeling**: Emails are manually labeled to identify banking-related content.
3. **Model Training**: A Naive Bayes classifier is trained on the labeled dataset.
4. **Gmail Watch Setup**: Gmail watch is configured to send Pub/Sub messages on new emails.
5. **Listener**: A Pub/Sub subscriber listens for incoming messages and triggers classification.
6. **Email Classification**: New emails are classified and tagged or handled accordingly.


## Adapting for Your Use Case

This project was trained using a manually labeled dataset of approximately 2,000 personal Gmail messages. The primary focus was to identify and classify emails related to banking and finance.

If you're interested in detecting other types of emails (e.g., job offers, subscriptions, travel confirmations), you can extend this project by:

- Collecting and labeling a sample of your own emails
- Retraining the model with new categories
- Updating the logic in `main.py` to support multi-label classification or filtering

The classification model is intentionally simple (Naive Bayes) to keep the project lightweight and easy to adapt. 



## Setup Instructions

1. **Clone the repository**
git clone https://github.com/Kanha-Sodani/gmail_classifier.git
cd gmail_classifier

2. **Create and activate a virtual environment**
python3 -m venv venv
source venv/bin/activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Prepare your Gmail API credentials**

To allow the app to access your Gmail account and receive email notifications, you'll need to set up credentials in Google Cloud:

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable the **Gmail API** and **Pub/Sub API**
- Navigate to **APIs & Services > Credentials**
- Click **"Create Credentials" > "OAuth client ID"**
  - Choose **Desktop App**
  - Download the `credentials.json` file
- Place this file in a folder named `credentials/` (which is excluded by `.gitignore`)
- The first time you run the project, you'll be prompted to log in and authorize access — this will create a `token.pickle` file that stores your access token

Make sure your Pub/Sub topic is also configured in GCP and that Gmail has permission to publish to it.

5. **Set environment variables**

- Create a `.env` file using the provided `.env.template`
- Add your Gmail and GCP configuration to the file

6. **Set up Gmail Watch** Run the Gmail watch setup script: python set_watch.py

7. **Start the listener** Run the listener to begin real-time email classification: python listener.py

## Security

This repository does not contain any personal data or credentials. Sensitive files such as `.env`, `token.pickle`, and Gmail credentials are excluded via `.gitignore`.
