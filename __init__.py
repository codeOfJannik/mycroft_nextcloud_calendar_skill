from mycroft import MycroftSkill, intent_file_handler
from .CalDavInterface import *
import calendar

class NextcloudCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.caldav_interface = None

    def initialize(self):
        self.caldav_interface = CalDavInterface(
            self.settings.get('url'),
            self.settings.get('username'),
            self.settings.get('password')
        )

    # @intent_file_handler('calendar.nexcloud.intent')
    # def handle_calendar_nexcloud(self, message):
    #     data = {"date": "June 29, 2020", "time": "4 pm", "title": "Speech Interaction class"}
    #     self.speak_dialog('calendar.nexcloud', data)
    #
    # @intent_file_handler('cancel.appointments.intent')
    # def handle_cancel_multiple_appointments(self, message):
    #     date = message.data.get('date') # TODO: parse date
    #     # TODO: get all appointments on date
    #     # TODO: Delete all appointments and respond with confirmation on cancellation OR
    #     # TODO: respond with summary of appointments that will be deleted and ask for confirmation
    #
    # @intent_file_handler('get.appointment.date.intent')
    # def handle_appointment_request_for_datetime(self, message):
    #     date = message.data.get('date')  # TODO: parse date
    #     time = message.data.get('time') # TODO: parse time
    #     # TODO: implement interface logic

    @intent_file_handler('get.next.appointment.intent')
    def handle_get_next_appointment(self, message):
        next_event = self.caldav_interface.get_next_event()
        title = next_event["title"]
        startdate_time = next_event["starttime"]
        date_formatted = "{month} {day}, {year}".format(
            month=calendar.month_name[startdate_time.month],
            day=startdate_time.day,
            year=startdate_time.year
        )
        time_formatted = startdate_time.strftime("%I:%M %p")
        data = {
            "date": date_formatted,
            "time": time_formatted,
            "title": title
        }
        self.speak_dialog('next.appointment.details.dialog', data)


def create_skill():
    return NextcloudCalendar()
