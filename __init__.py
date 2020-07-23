"""A Mycroft AI skill for voice interaction with a Nextcloud calendar.

Main class 'NextcloudCalendar' contains intent handler
for intent files in directory locale/en-us. Each intent
handler gets the relevant calendar information for
the specific intent and chooses a suitable response
from the dialog files.
"""
import calendar
from  datetime import datetime
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util import LOG
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.parse import extract_datetime
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
        startdatetime.hour == 0
        and startdatetime.minute == 0
        and startdatetime.second == 0
        and enddatetime.hour == 0
        and enddatetime.minute == 0
        and enddatetime.second == 0
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
        elif not password:
            self.speak_dialog('err.nextcloud.settings.missing')
            return False
        elif not url:
            self.speak_dialog('err.nextcloud.settings.missing')
            return False

        self.caldav_interface = CalDavInterface(
            self.settings.get('url'),
            self.settings.get('username'),
            self.settings.get('password')
        )
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

        # because we are using Python v3.7.3
        # the order of the keys of the dictionary is the the same as inserted,
        # so we can iterate over the keys to generate the correct dialog filenames
        for key in data:
            dialog_filename += "." + key
        self.speak_dialog(dialog_filename, data)

    @intent_handler('get.appointment.date.intent')
    def handle_get_appointment_date(self, message):
        """

        :param message:
        :return:
        """
        LOG.debug(f"Intent message {message}")
        date = extract_datetime(message, datetime.today())
        requested_date, requested_time = format_datetime_for_output(date)
        events = self.caldav_interface.get_events_for_date(date)
        if len(events) == 0:
            self.speak_dialog("no.events.on.date", {"date": requested_date})
        else:
            self.speak_dialog("number.events.on.date", {"date": requested_date, "number": len(events)})
            if self.ask_yesno("list.events.of.date", {"date": requested_date}) == "yes":
                self.speak_dialog("events.on.date", {"date": requested_date})
                for event in events:
                    title = event["title"]
                    startdate_time = event["starttime"]
                    enddate_time = event["endtime"]
                    _, starttime_formatted = format_datetime_for_output(startdate_time)
                    _, endtime_formatted = format_datetime_for_output(enddate_time)

                    self.speak_dialog(
                        "event.details",
                        {"title": title,
                         "starttime": starttime_formatted,
                         "endtime": endtime_formatted}
                    )


def create_skill():
    """

    :return:
    """
    return NextcloudCalendar()