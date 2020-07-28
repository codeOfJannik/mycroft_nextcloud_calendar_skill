"""A Mycroft AI skill for voice interaction with a Nextcloud calendar.

Main class 'NextcloudCalendar' contains intent handler
for intent files in directory locale/en-us. Each intent
handler gets the relevant calendar information for
the specific intent and chooses a suitable response
from the dialog files.
"""
import calendar
from datetime import datetime

from mycroft import MycroftSkill, intent_handler
from mycroft.util.format import nice_time, nice_date
from mycroft.util.parse import extract_datetime
from mycroft.util.time import default_timezone

from .cal_dav_interface import CalDavInterface


def format_datetime_for_output(date_time):
    """
    Formats a datetime object to string objects for date and time, that can be used in speech output
    :param date_time: datetime object that should be formatted
    :return: a string for the date and the time each
    """
    date_formatted = "{month} {day}, {year}".format(
        month=calendar.month_name[date_time.month],
        day=date_time.day,
        year=date_time.year
    )
    time_formatted = date_time.strftime("%I:%M %p")
    return date_formatted, time_formatted


def is_multiple_fulldays_event(startdatetime, enddatetime):
    """
    Checks if an event is a multi-day & full-day event
    by comparing start datetime and end datetime of the event
    :param startdatetime: Start datetime of the event
    :param enddatetime: End datetime of the event
    :return: [bool] True if multi-day & full-day
    """
    fullday = is_fullday_event(startdatetime, enddatetime)
    delta = enddatetime - startdatetime
    return fullday and delta.days > 1


def is_fullday_event(startdatetime, enddatetime):
    """
    Checks if an event is a full-day event by comparing start datetime and end datetime of the event
    :param startdatetime: Start datetime of the event
    :param enddatetime: End datetime of the event
    :return: [bool] True if full-day
    """
    return (
        startdatetime.hour == 0 and
        startdatetime.minute == 0 and
        startdatetime.second == 0 and
        enddatetime.hour == 0 and
        enddatetime.minute == 0 and
        enddatetime.second == 0
    )


class NextcloudCalendar(MycroftSkill):
    """
    The class contains intent handlers
    for intent files in directory locale/en-us. Each intent
    handler gets the relevant calendar information for
    the specific intent and chooses a suitable response
    from the dialog files.
    """

    def __init__(self):
        MycroftSkill.__init__(self)
        self.caldav_interface = None

    def initialize(self):
        """
        Checks if the credentials (url, username and password) are set on Mycroft website.
        If not, a corresponding dialog is output.
        If the credentials are present, a CalDavInterface instance
        is created
        :return: [bool] False if credentials are not set
        """
        username = self.settings.get('username')
        password = self.settings.get('password')
        url = self.settings.get('url')

        if not username:
            self.speak_dialog('err.nextcloud.settings.missing')
            return False
        if not password:
            self.speak_dialog('err.nextcloud.settings.missing')
            return False
        if not url:
            self.speak_dialog('err.nextcloud.settings.missing')
            return False

        self.caldav_interface = CalDavInterface(
            self.settings.get('url'),
            self.settings.get('username'),
            self.settings.get('password'),
            default_timezone()
        )
        self.log.info(f"Initialized CaldDavInterface with timezone {default_timezone()}")
        return True

    @intent_handler('get.next.appointment.intent')
    def handle_get_next_appointment(self, message):
        """
        Generates the respond for the intent asking for the next appointment
        in the connected Nextcloud calendar.
        :param message: The speech input message. Unused in this method
        """
        del message  # unused by handler
        next_event = self.caldav_interface.get_next_event()
        data = {}
        dialog_filename = "next.appointment"
        if next_event is not None:
            title = next_event["title"]
            startdate_time = next_event["starttime"]
            enddate_time = next_event["endtime"]
            startdate_formatted, starttime_formatted = format_datetime_for_output(startdate_time)
            enddate_formatted, _ = format_datetime_for_output(enddate_time)
            data["startdate"] = startdate_formatted
            if is_multiple_fulldays_event(startdate_time, enddate_time):
                data["enddate"] = enddate_formatted
            else:
                if not is_fullday_event(startdate_time, enddate_time):
                    data["time"] = starttime_formatted

            if title is not None:
                data["title"] = title

        # because we are using Python v3.7.x
        # the order of the keys of the dictionary is the the same as inserted,
        # so we can iterate over the keys to generate the correct dialog filenames
        for key in data:
            dialog_filename += "." + key
        self.speak_dialog(dialog_filename, data)

    @intent_handler('get.appointment.date.intent')
    def handle_get_appointment_date(self, message):
        """
        Handles the intent asking for events on a specific date.
        Checks the calendar on the specified date first,
        then responses with the number of planned events.
        If it's not 0, the user is asked if the events
        should be listed. IF the user responds with 'yes'
        all events are listed with title, start and end time.
        :param message: The speech input message. Used to extract the specified date
        """
        self.log.info(f"Intent message: {message.data['utterance']}")
        extracted_date = extract_datetime(message.data['utterance'], datetime.today())[0]
        self.log.debug(f"Extracted date(s): {extracted_date}")
        events = self.caldav_interface.get_events_for_date(extracted_date)
        self.log.debug(f"Events on {extracted_date}: {events}")

        if len(events) == 0:
            self.speak_dialog(
                "no.events.on.date",
                {"date": nice_date(extracted_date, now=datetime.today())}
            )
        else:
            self.speak_dialog(
                "number.events.on.date",
                {
                    "date": nice_date(extracted_date, now=datetime.today()),
                    "number_of_appointments": len(events),
                    "plural": "s" if len(events) > 1 else ""
                }
            )
            list_events = self.ask_yesno(
                "list.events.of.date",
                {"date": nice_date(extracted_date, now=datetime.today())}
            )
            if list_events == "yes":
                self.speak_dialog(
                    "events.on.date",
                    {"date": nice_date(extracted_date, now=datetime.today())}
                )
                for event in events:
                    title = event["title"]
                    startdate_time = event["starttime"]
                    enddate_time = event["endtime"]

                    self.speak_dialog(
                        "event.details",
                        {
                            "title": title,
                            "starttime": nice_time(startdate_time, use_ampm=True),
                            "endtime": nice_time(enddate_time, use_ampm=True)
                        }
                    )


def create_skill():
    """
    Creates an instance of the skill class. Required from MycroftAI
    :return: instance of skill class
    """
    return NextcloudCalendar()
