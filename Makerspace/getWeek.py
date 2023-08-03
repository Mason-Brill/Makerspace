#######################################################################
# getWeek
#
# This library includes functions to get and format weeks of time.
#
# REFERENCES
# [1] https://stackoverflow.com/questions/2003841/how-can-i-get-the-current-week-using-python
# [2] https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# [3] https://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python
#######################################################################
from datetime import timedelta, datetime


# takes a datetime object [R1]
# returns a list of datetime objects for the week of the provided date
# starting with Sunday
def getWeek(datetime_object):
    # determine date of the first day (Sunday) of the given date
    day_index = (datetime_object.weekday() + 1) % 7
    start_date = datetime_object - timedelta(days=day_index)

    # create a list of dates of for the provided date (starting with Sunday)
    week = []
    for i in range(7):
        week.append(start_date)
        start_date += timedelta(days=1)

    # return a list of datetime objects for the provided date
    return week


# returns a list containing the current week's dates starting with Sunday
def getCurrentWeek():
    date_today = datetime.now()
    return getWeek(date_today)


# returns a list containing next week's dates starting with Sunday
def getNextWeek():
    date_today = datetime.now()
    next_week = date_today + timedelta(days=7)
    return getWeek(next_week)


# returns a list containing the dates of the previous week starting with Sunday
def getPreviousWeek():
    # determine date of the first day (Sunday) of the previous week
    date_today = datetime.now()
    previous_week = date_today - timedelta(days=7)
    return getWeek(previous_week)


# takes a list of datetime objects
# a string with the date's format specifiers [R2]
# return a list of the dates in the specified format
def formatDates(date_list, date_format):
    return [day.strftime(date_format) for day in date_list]


# takes a list of datetime objects
# returns a list of this week's dates as an RFC3339 timestamp [R3]
def RFC3339(date_list):
    return [day.isoformat() + 'Z' for day in date_list]


# takes a list of formatted dates
# returns html formatted string of dates
def createHTMLParagraphedDates(week):
    html_dates = ''
    for day in week:
        html_dates += "<p>" + day + "</p>"
    return html_dates


if __name__ == '__main__':
    # EXAMPLE to create a datetime object and use it to get the associated week
    year, month, _day, hours, minutes = 2023, 2, 28, 14, 30
    date = datetime(year, month, _day, hours, minutes)
    random_week = getWeek(date)
    print("example of {type(date)} object for:")
    print(f"day: {_day}, month: {month}, year: {year}, hours: {hours}, minutes: {minutes}")
    print(f"prints as: {date}")
    print(f"the associated week is: {random_week}")

    # EXAMPLE to get a list of days in a week
    last_week = getPreviousWeek()
    this_week = getCurrentWeek()
    following_week = getNextWeek()
    print(f"Example to get a list of datetime objects for days in a week:")
    print(f"last week: {last_week}")
    print(f"this week: {this_week}")
    print(f"next week: {following_week}")

    # EXAMPLE to format a list of datetime objects [see R2 for format specifiers]
    my_format = "%d %B %Y"
    formatted_week = formatDates(this_week, my_format)
    print(f"%d %B %Y formatted week: {formatted_week}")

    # EXAMPLE to format a list of datetime objects in RFC3339
    rfc3339_week = RFC3339(this_week)
    print(f"RFC3339 formatted week: {rfc3339_week}")

    # EXAMPLE showing how to create html paragraph formatted dates
    html = createHTMLParagraphedDates(formatted_week)
    print(html)
