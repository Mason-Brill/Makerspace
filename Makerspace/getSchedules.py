#######################################################################
# getSchedules
#
# This library includes functions to create and format the operational
# hours of the makerspace for a given week or the hours a worker is
# scheduled to work during a given week.
#######################################################################
import calendarIDs
import calendarEvents
import getWeek


# takes a list of lists where each list contains two datetime objects
# that represent a start and end time
# --> overlapping start and end times are combined into a single start and end time
# returns the condensed list of lists of datetime objects
def condenseSchedule(worker_hours):
    # sort worker hours by start time
    worker_hours = sorted(worker_hours, key=lambda x: x[0])

    # condense worker schedule
    condensed_schedule = [worker_hours[0]]
    START = 0   # shift start
    END = 1     # shift end
    for shift in worker_hours:
        close_time = condensed_schedule[-1][END]
        if shift[START] <= close_time and shift[END] > close_time:
            condensed_schedule[-1][END] = shift[END]
        elif shift[START] > close_time:
            condensed_schedule.append(shift)
    return condensed_schedule


# TODO -> test whether this function works for a list that contains multiple weeks
# TODO -> add "closed" to any dates without open hours ???
# takes a list of lists where each list contains two datetime objects
# returns a list of formatted hours in the form: dayOfWeek start_time - end_time
def formatSchedule(worker_hours):
    # sort worker hours by start time
    worker_hours = sorted(worker_hours, key=lambda x: x[0])

    # format worker hours
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    is_already_open = [False, False, False, False, False, False, False]
    schedule = []
    for shift in worker_hours:
        if shift[0].strftime("%A") == days[0]:
            if is_already_open[0]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[0] = True
                schedule.append(f'{days[0]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[1]:
            if is_already_open[1]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[1] = True
                schedule.append(f'{days[1]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[2]:
            if is_already_open[2]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[2] = True
                schedule.append(f'{days[2]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[3]:
            if is_already_open[3]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[3] = True
                schedule.append(f'{days[3]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[4]:
            if is_already_open[4]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[4] = True
                schedule.append(f'{days[4]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[5]:
            if is_already_open[5]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[5] = True
                schedule.append(f'{days[5]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
        if shift[0].strftime("%A") == days[6]:
            if is_already_open[6]:
                schedule.append(f'{"":<10}{shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')
            else:
                is_already_open[6] = True
                schedule.append(f'{days[6]:<9} {shift[0].strftime("%I:%M %p")} - {shift[1].strftime("%I:%M %p")}')

    return schedule


# takes a list of worker names and a time frame where the time frame
# is either a list of datetime objects or a predefined option
# returns a list of formatted hours in the form: dayOfWeek start_time - end_time
def createSchedule(workers, time_frame="this_week"):
    # determine and RFC3339 format schedule time frame
    if time_frame == "previous_week":
        dates = getWeek.RFC3339(getWeek.getPreviousWeek())
    elif time_frame == "this_week":
        dates = getWeek.RFC3339(getWeek.getCurrentWeek())
    elif time_frame == "next_week":
        dates = getWeek.RFC3339(getWeek.getNextWeek())
    elif type(time_frame) is list:
        dates = getWeek.RFC3339(time_frame)
    else:
        return None

    # get work calendar ids
    worker_ids = [calendarIDs.getCalendarID(worker) for worker in workers]

    # get and format worker's schedule
    events = calendarEvents.getCalendarEvents(worker_ids, dates[0], dates[6])
    event_times = calendarEvents.getEventTimes(events)
    schedule = condenseSchedule(event_times)
    formatted_schedule = formatSchedule(schedule)

    return formatted_schedule


# takes a list of formatted hours
# returns html formatted string of hours using <pre> tag to maintain formatting spaces
def html_format(hours_of_operation):
    html_schedule = ""
    for line in hours_of_operation:
        html_schedule += f"<pre>{line}</pre>"
    return html_schedule


if __name__ == '__main__':
    from datetime import datetime
    # EXAMPLE to test condenseSchedule()
    # create a list of lists where each list contains two datetime objects
    worker_shifts = [[datetime(2023, 3, 2, 10, 15), datetime(2023, 3, 2, 14, 45)],
                     [datetime(2023, 2, 28, 17, 0), datetime(2023, 2, 28, 19, 30)],
                     [datetime(2023, 2, 27, 12, 35), datetime(2023, 2, 27, 15, 0)],
                     [datetime(2023, 3, 2, 7, 27), datetime(2023, 3, 2, 8, 36)],
                     [datetime(2023, 3, 1, 16, 59), datetime(2023, 3, 1, 20, 42)],
                     [datetime(2023, 3, 3, 14, 30), datetime(2023, 3, 3, 16, 12)],
                     [datetime(2023, 3, 2, 16, 30), datetime(2023, 3, 2, 18, 45)],
                     [datetime(2023, 3, 2, 8, 30), datetime(2023, 3, 2, 11, 45)]]
    # condense the schedule to combine overlapping start/end times
    condensed_shifts = condenseSchedule(worker_shifts)
    # format condensed schedule
    worker_schedule = formatSchedule(condensed_shifts)
    # print schedule
    print("example to demonstrate condensed hours:")
    for hours_open in worker_schedule:
        print(hours_open)

    # EXAMPLE demonstrating how to create a condensed schedule for all workers
    worker_list = ['Lorielle Raab', 'Mason Brill', 'Abhigyan Tripathi']
    weekly_schedule = createSchedule(worker_list, time_frame="this_week")
    print("\nexample to demonstrate creating a schedule for all workers:")
    for hours_open in weekly_schedule:
        print(hours_open)

    # EXAMPLE demonstrating how to create HTML for a schedule
    html = html_format(weekly_schedule)
    print("\nexample to demonstrate HTML output of schedule")
    print(html)

    # EXAMPLE demonstrating how to create a schedule for a single worker
    weekly_schedule = createSchedule(['Lorielle Raab'], time_frame="this_week")
    print("\nexample to demonstrate creating a schedule for a single worker:")
    for hours_open in weekly_schedule:
        print(hours_open)
