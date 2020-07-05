from mycroft import MycroftSkill, intent_file_handler


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

