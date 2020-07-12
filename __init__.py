from mycroft import MycroftSkill, intent_file_handler
from .CalDavInterface import *
import calendar


def format_datetime_for_output(date_time):
    date_formatted = "{month} {day}, {year}".format(
        month=calendar.month_name[date_time.month],
        day=date_time.day,
        year=date_time.year
    )
    time_formatted = date_time.strftime("%I:%M %p")
    return date_formatted, time_formatted


def is_multiple_fulldays_event(startdatetime, enddatetime):
    fullday = is_fullday_event(startdatetime, enddatetime)
    delta = enddatetime - startdatetime
    return fullday and delta.days > 1


def is_fullday_event(startdatetime, enddatetime):
    return (
        startdatetime.hour == 0
        and startdatetime.minute == 0
        and startdatetime.second == 0
        and enddatetime.hour == 0
        and enddatetime.minute == 0
        and enddatetime.second == 0
    )


class NextcloudCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.caldav_interface = None

    def initialize(self):
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

    @intent_file_handler('get.next.appointment.intent')
    def handle_get_next_appointment(self, message):
        next_event = self.caldav_interface.get_next_event()
        data = {}
        dialog_filename = "next.appointment"
        if next_event is not None:
            title = next_event["title"]
            startdate_time = next_event["starttime"]
            enddate_time = next_event["endtime"]
            startdate_formatted, starttime_formatted = format_datetime_for_output(startdate_time)
            enddate_formatted, endtime_formatted = format_datetime_for_output(enddate_time)
            data["startdate"] = startdate_formatted
            if is_multiple_fulldays_event(startdate_time, enddate_time):
                data["enddate"] = enddate_formatted
            else:
                if not is_fullday_event(startdate_time, enddate_time):
                    data["time"] = starttime_formatted

            if title is not None:
                data["title"] = title

        # because we are using Python v3.7.3 the order of the keys of the dictionary is the the same as inserted,
        # so we can iterate over the keys to generate the correct dialog filenames
        for key in data.keys():
            dialog_filename += ".".join(key)
        self.speak_dialog(dialog_filename, data)


def create_skill():
    return NextcloudCalendar()
