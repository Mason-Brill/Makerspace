#######################################################################
# calendarEvents
#
# This library connects to the Google calendar api and gets all
# calendar events associated with the provided calendar id for the
# specified dates [see R2 for details on what is included in the
# calendar event list].
#
# REFERENCES
# [1] https://developers.google.com/calendar/api/quickstart/python
# [2] https://developers.google.com/calendar/api/v3/reference/events/list
#######################################################################
import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# takes a list of calendar ids, a start date and an end date
# NOTE: the dates must be formatted in RFC3339
# returns a list of calendar events for provided details
def getCalendarEvents(calendar_ids, start_date, end_date):
    creds = None
    # the token.json file is created the first time the program is run
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
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

        # get a list of calendar events during provided time period for each calendar id [R2]
        page_token = None
        events = []
        for item in calendar_ids:
            while True:
                calendar_events = service.events().list(calendarId=item, timeMin=start_date, timeMax=end_date,
                                                        singleEvents=True, orderBy='startTime',
                                                        pageToken=page_token).execute()
                page_token = calendar_events.get('nextPageToken')
                if not page_token:
                    break

            # each calendar id is its own list within the events list
            events.append(calendar_events.get('items', []))

        # combine separate calendar event lists into a single list
        return [event for event_list in events for event in event_list]

    except HttpError as error:
        print('An error occurred: %s' % error)


# takes a list of calendar events
# returns a list of lists where each list contains two datetime objects:
# [0] when the event starts and [1] when the event ends
def getEventTimes(events):
    event_times = []
    for event in events:
        event_start = event['start']['dateTime']
        event_start = datetime.strptime(event_start[:10] + event_start[11:19], "%Y-%m-%d%H:%M:%S")
        event_end = event['end']['dateTime']
        event_end = datetime.strptime(event_end[:10] + event_end[11:19], "%Y-%m-%d%H:%M:%S")
        event_times.append([event_start, event_end])
    return event_times


if __name__ == '__main__':
    import calendarIDs
    import getWeek
    # EXAMPLE to get calendar events
    # first get calendar IDs
    workers = ['Lorielle Raab', 'Mason Brill', 'Abhigyan Tripathi']
    calendarIDs = [calendarIDs.getCalendarID(worker) for worker in workers]
    # second get RFC3339 formatted start and end dates
    current_week = getWeek.RFC3339(getWeek.getCurrentWeek())
    # get calendar event list
    list_of_events = getCalendarEvents(calendarIDs, current_week[0], current_week[6])
    print("Example showing contents of calendar event list:")
    for activity in list_of_events:
        print(activity)

    # EXAMPLE to get event start and end times
    time_of_events = getEventTimes(list_of_events)
    print("Example showing event start and end times:")
    for time in time_of_events:
        print(time)
