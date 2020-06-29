from mycroft import MycroftSkill, intent_file_handler


class NexcloudCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('calendar.nexcloud.intent')
    def handle_calendar_nexcloud(self, message):
        data = {"date": "June 29, 2020", "time": "4 pm", "title": "Speech Interaction class"}
        self.speak_dialog('calendar.nexcloud', data)


def create_skill():
    return NexcloudCalendar()

