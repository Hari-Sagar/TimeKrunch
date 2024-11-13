
import os.path
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarHelper:
  def __init__(self):
    creds = None

    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    
      with open("token.json", "w") as token:
        token.write(creds.to_json())

  
    self.service = build("calendar", "v3", credentials=creds)
  
  def create_event(self, task):
    print(task.due_date)
    print(task.duration)
    print("#####################" + (datetime.datetime.fromisoformat(task.due_date) + timedelta(hours=task.duration)).isoformat())
    
    event = {
      'summary': task.title,
      'description': task.description,
      'start': {
        'dateTime': task.due_date,
        'timeZone': 'America/Los_Angeles'
            },
      'end': {
        'dateTime': ((datetime.datetime.fromisoformat(task.due_date) + timedelta(hours=task.duration)).isoformat()),
        'timeZone': 'America/Los_Angeles'
      },  
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 8 * 60}
        ],
      },
      "extendedProperties": {
      "private": {
        'watermark': 'Calendar Tag'
      },

      }
    }

    event = self.service.events().insert(calendarId='primary', body=event).execute()



  def delete_events(self):
    now = (datetime.datetime.now(datetime.timezone.utc) - relativedelta(year=1)).isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        self.service.events()
        .list(
            calendarId="primary",
            maxResults=1000,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    for event in events:
      if 'extendedProperties' in event and 'watermark' in event['extendedProperties']['private']:
        self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
