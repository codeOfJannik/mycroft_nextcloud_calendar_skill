import caldav
from datetime import datetime
import icalendar
import pytz

utc = pytz.UTC

def delete_events(events):
    for event in events:
        event.delete()


def parse_ics_events(events):
    parsed_events = []
    for event in events:
        cal = icalendar.Calendar.from_ical(event.data, True)
        [parsed_events.append(get_event_details(e)) for e in cal[0].walk("vevent")]
    return parsed_events


def get_event_details(event):
    start = event["DTSTART"].dt
    end = event["DTEND"].dt
    title = str(event["SUMMARY"])
    return {"title": title, "starttime": start, "endtime": end}


class CalDavInterface:
    def __init__(self, url, username, password):
        self.client = caldav.DAVClient(
            url=url,
            username=username,
            password=password
        )
        self.calendar = self.get_calendar()

    def get_calendar(self):
        my_principal = self.client.principal()
        return my_principal.calendars()[0]

    def get_events_for_timeperiod(self, startdate, enddate):
        events = self.calendar.date_search(start=startdate, end=enddate, expand=True)
        return parse_ics_events(events)

    def get_next_event(self):
        all_events = self.calendar.events()
        parsed_events = parse_ics_events(all_events)
        sorted_events = sorted(parsed_events, key=lambda i: i["starttime"])
        for event in sorted_events:
            starttime = event["starttime"]
            now = datetime.today()
            current_time = now.replace(tzinfo=starttime.tzinfo)
            if starttime > current_time:
                return event
