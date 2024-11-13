
import os.path
import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


print(datetime.datetime.now().isoformat())
print((datetime.datetime.now() + timedelta(hours=1)).isoformat())




