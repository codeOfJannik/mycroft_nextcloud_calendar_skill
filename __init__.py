from mycroft import MycroftSkill, intent_file_handler
import caldav

class NextcloudInterface:
    def __init__(self):
        # TODO: where to store credentials?
        self.client = caldav.DAVClient() #TODO: add credentials
        self.calendars = self.fetch_calendars()

    def fetch_calendars(self):
        my_principal = self.client.principal()
        return my_principal.calendars()

    def get_events_for_timeperiod(self, calendar, startdate, enddate):
        events = calendar.date_search(start=startdate, end=enddate, expand=True)

    def delete_events(self, events):
        for event in events:
            event.delete()

class NexcloudCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('calendar.nexcloud.intent')
    def handle_calendar_nexcloud(self, message):
        data = {"date": "June 29, 2020", "time": "4 pm", "title": "Speech Interaction class"}
        self.speak_dialog('calendar.nexcloud', data)

    @intent_file_handler('cancel.appointments.intent')
    def handle_cancel_multiple_appointments(self, message):
        date = message.data.get('date') # TODO: parse date
        # TODO: get all appointments on date
        # TODO: Delete all appointments and respond with confirmation on cancellation OR
        # TODO: respond with summary of appointments that will be deleted and ask for confirmation


def create_skill():
    return NexcloudCalendar()

