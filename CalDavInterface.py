import caldav
import json
from datetime import datetime
from icalendar import Calendar, Event


def delete_events(events):
    for event in events:
        event.delete()


def parse_ics_events(events):
    parsed_events = []
    for event in events:
        cal = Calendar.from_ical(event.data, True)
        [parsed_events.append(get_event_details(e)) for e in cal[0].walk("vevent")]
    return parsed_events

def get_event_details(event):
    start = event["DTSTART"].dt
    end = event["DTEND"].dt
    title = str(event["SUMMARY"])
    return {"title": title, "starttime": start, "endtime": end}

class CalDavInterface:
    def __init__(self):
        with open("credentials.json") as credentials_file:
            credentials = json.load(credentials_file)
            self.client = caldav.DAVClient(
                url=credentials["url"],
                username=credentials["username"],
                password=credentials["password"]
            )
            self.calendar = self.get_calendar()

    def get_calendar(self):
        my_principal = self.client.principal()
        return my_principal.calendars()[0]

    def get_events_for_timeperiod(self, calendar, startdate, enddate):
        events = calendar.date_search(start=startdate, end=enddate, expand=True)
        return parse_ics_events(events)

