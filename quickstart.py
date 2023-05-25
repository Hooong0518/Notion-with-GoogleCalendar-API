from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import pytz
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 權限主程式
def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('json/token.json'):
        creds = Credentials.from_authorized_user_file('json/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'json/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('json/token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service

    except HttpError as error:
        print('An error occurred: %s' % error)

# 建立事件
def new_event(calendar_id, event):
    service = main()
    result = service.events().insert(calendarId=calendar_id, body=event).execute()
    return result.get('id')

# 刪除事件
def delete_event(calendar_id, eventId):
    service = main()
    result = service.events().delete(calendarId=calendar_id, eventId=eventId).execute()
    return result

# 更新事件
def update_event(calendar_id, eventId, event):
    service = main()
    result = service.events().update(calendarId=calendar_id, eventId=eventId, body=event).execute()
    return result

# 查詢事件
def get_event(calendar_id,eventId):
    service = main()
    event = service.events().get(calendarId=calendar_id, eventId=eventId).execute()
    return event

# 取得日曆內今日後的所有事件
def get_event_list(calandarID):
    service = main()
    result = []
    page_token = None
    taipei_tz = pytz.timezone('Asia/Taipei')
    now = datetime.datetime.now(taipei_tz)
    midnight = now.replace(hour=23, minute=59, second=59, microsecond=0)
    today = midnight.isoformat() # 將 datetime 物件轉換為 ISO 8601 格式的字串
    while True:
        events = service.events().list(calendarId=calandarID, pageToken=page_token, timeMin = today).execute()
        for event in events['items']:
            result.append(event['id'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return result

# 移動事件
def move_event(calendar_id_old, calendar_id_new, eventID):
    service = main()
    result = service.events().move(
        calendarId=calendar_id_old, eventId=eventID,
        destination=calendar_id_new).execute()
    return result
