#######################################################################
# calendarIDs
#
# This library connects to the Google calendar api and gets all
# calendar ids associated with the account [see R2 for details on
# what is included in the calendar list].
#
# It provides a function to get the calendar id for a specific
# calendar name.
#
# REFERENCES
# [1] https://developers.google.com/calendar/api/quickstart/python
# [2] https://developers.google.com/calendar/api/v3/reference/calendarList/list#python
# [3] https://www.w3schools.com/python/gloss_python_raise.asp
#######################################################################
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# returns calendar list from google calendar api
def getCalendarList():
    creds = None
    # the token.json file is created the first time the program is run
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)

        # get a list of all calendars [R2]
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        return calendar_list

    except HttpError as error:
        print('An error occurred: %s' % error)


# takes calendar name
# returns calendar id associated with provided name
def getCalendarID(name):
    calendar_list = getCalendarList()
    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary'] == name:
            calendar_id = calendar_list_entry['id']
            return calendar_id
    # name not found
    return None


if __name__ == '__main__':
    # EXAMPLE to get single worker id
    worker = 'Abhigyan Tripathi'
    calendarID = getCalendarID(worker)
    print(f"calendar id for {worker}: {calendarID}\n")

    # EXAMPLE to get multiple worker ids
    workers = ['Lorielle Raab', 'Mason Brill', 'Abhigyan Tripathi']
    calendarIDs = [getCalendarID(worker) for worker in workers]
    print("calendar ids for multiple workers:")
    for i in range(len(workers)):
        print(f"calendar id for {workers[i]}: {calendarIDs[i]}")
