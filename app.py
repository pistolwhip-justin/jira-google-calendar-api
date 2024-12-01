import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from jira import JIRA
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Jira Configuration
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_SERVER_URL = os.getenv('JIRA_SERVER_URL')

# Initialize Jira Client
jira_client = JIRA(
    server=JIRA_SERVER_URL,
    basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN)
)

# Google Calendar Configuration
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

def get_google_calendar_service():
    """Initialize Google Calendar service."""
    try:
        creds = Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS_PATH)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        logger.error(f"Google Calendar authentication error: {e}")
        return None

@app.route('/sync/jira-to-calendar', methods=['POST'])
def sync_jira_to_calendar():
    """Sync Jira issues to Google Calendar."""
    try:
        # Get Jira issues
        jira_issues = jira_client.search_issues('updated >= -1w')
        
        calendar_service = get_google_calendar_service()
        if not calendar_service:
            return jsonify({"error": "Google Calendar authentication failed"}), 401

        for issue in jira_issues:
            # Create calendar event from Jira issue
            event = {
                'summary': issue.fields.summary,
                'description': issue.fields.description or '',
                'start': {
                    'dateTime': issue.fields.created,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (datetime.datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z') + datetime.timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                }
            }
            
            calendar_service.events().insert(calendarId='primary', body=event).execute()
        
        return jsonify({"message": f"Synced {len(jira_issues)} issues to calendar"}), 200
    
    except Exception as e:
        logger.error(f"Sync error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/sync/calendar-to-jira', methods=['POST'])
def sync_calendar_to_jira():
    """Sync Google Calendar events to Jira."""
    try:
        calendar_service = get_google_calendar_service()
        if not calendar_service:
            return jsonify({"error": "Google Calendar authentication failed"}), 401

        # Get calendar events from last week
        now = datetime.datetime.utcnow()
        week_ago = now - datetime.timedelta(days=7)
        
        events_result = calendar_service.events().list(
            calendarId='primary', 
            timeMin=week_ago.isoformat() + 'Z',
            maxResults=100, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        for event in events:
            # Create Jira issue from calendar event
            issue_dict = {
                'project': {'key': 'YOUR_PROJECT_KEY'},  # Replace with your Jira project key
                'summary': event.get('summary', 'Untitled Event'),
                'description': event.get('description', ''),
                'issuetype': {'name': 'Task'}  # Adjust issue type as needed
            }
            
            jira_client.create_issue(fields=issue_dict)
        
        return jsonify({"message": f"Synced {len(events)} calendar events to Jira"}), 200
    
    except Exception as e:
        logger.error(f"Sync error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
