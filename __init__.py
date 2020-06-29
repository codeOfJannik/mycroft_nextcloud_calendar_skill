from mycroft import MycroftSkill, intent_file_handler


class NexcloudCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('calendar.nexcloud.intent')
    def handle_calendar_nexcloud(self, message):
        self.speak_dialog('calendar.nexcloud')


def create_skill():
    return NexcloudCalendar()

