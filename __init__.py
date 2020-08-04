"""A Mycroft AI skill for voice interaction with a Nextcloud calendar.

Main class 'NextcloudCalendar' contains intent handler
for intent files in directory locale/en-us. Each intent
handler gets the relevant calendar information for
the specific intent and chooses a suitable response
from the dialog files.
"""
import datetime as dt
from datetime import datetime
import re

from mycroft import MycroftSkill, intent_handler
from mycroft.util.format import nice_time, nice_date
from mycroft.util.parse import extract_datetime, extract_duration, extract_number
from mycroft.util.time import default_timezone

from .cal_dav_interface import CalDavInterface


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


def get_title_date_from_message(message):
    """
    Receives the message object of an intent handler and checks
    if it contains a title or date. If yes it is returned, else
    None is returned
    :param message: Message object of the intent handler
    :return: (title, date) if exists, (None, None) otherwise
    """
    title = None
    date = None
    if "title" in message.data:
        title = message.data["title"]
    if "date" in message.data:
        extracted = extract_datetime(message.data['utterance'], datetime.today())
        if extracted is not None:
            date = extracted[0]
    return title, date


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
        self.timezone = None

    def initialize(self):
        """
        Checks if the credentials (url, username and password) are set on Mycroft website.
        If not, a corresponding dialog will be displayed.
        If the credentials are present, a CalDavInterface instance
        is created.
        :return: [bool] False if credentials are not set
        """
        # TODO: check if get_intro_message() is suitable for our purpose
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

        self.timezone = default_timezone()

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
        Generates the response for the intent asking for the next appointment
        in the connected Nextcloud calendar.
        :param message: The speech input message. Unused in this method.
        """
        del message  # unused by handler
        next_event = self.caldav_interface.get_next_event()
        output_data = {}
        dialog_filename = "next.appointment"

        if next_event is not None:
            title = next_event["title"]
            startdate_time = next_event["starttime"]
            enddate_time = next_event["endtime"]
            output_data["startdate"] = nice_date(startdate_time)
            if is_multiple_fulldays_event(startdate_time, enddate_time):
                output_data["enddate"] = nice_date(enddate_time)
            else:
                if not is_fullday_event(startdate_time, enddate_time):
                    output_data["time"] = nice_time(startdate_time)

            if title is not None:
                output_data["title"] = title

        # because we are using Python v3.7.x
        # the order of the keys of the dictionary is the the same as inserted,
        # so we can iterate over the keys to generate the correct dialog filenames
        for key in output_data:
            dialog_filename += "." + key
        self.speak_dialog(dialog_filename, output_data)

    @intent_handler('get.appointment.date.intent')
    def handle_get_appointment_date(self, message):
        """
        Handles the intent asking for events on a specific date.
        Checks the calendar on the specified date first,
        then responses with the number of planned events.
        If it's not 0, the user is asked if the events
        should be listed. If the user responds with 'yes'
        all events are listed with title, start and end time.
        :param message: The speech input message. Used to extract the specified date
        """
        self.log.info(f"Intent message: {message.data['utterance']}")
        extracted_date = extract_datetime(message.data['utterance'], datetime.now(self.timezone))[0]
        self.log.debug(f"Extracted date(s): {extracted_date}")
        events = self.caldav_interface.get_events_for_date(extracted_date)
        self.log.debug(f"Events on {extracted_date}: {events}")

        if len(events) == 0:
            self.speak_dialog(
                "no.events.on.date",
                {"date": nice_date(extracted_date, now=datetime.now(self.timezone))}
            )
        else:
            self.speak_dialog(
                "number.events.on.date",
                {
                    "date": nice_date(extracted_date, now=datetime.now(self.timezone)),
                    "number_of_appointments": len(events),
                    "plural": "s" if len(events) > 1 else ""
                }
            )
            list_events = self.ask_yesno(
                "list.events.of.date",
                {"date": nice_date(extracted_date, now=datetime.now(self.timezone))}
            )
            if list_events == "yes":
                self.speak_dialog(
                    "events.on.date",
                    {"date": nice_date(extracted_date, now=datetime.now(self.timezone))}
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

    @intent_handler('delete.event.intent')
    def handle_delete_event(self, message):
        """
        Handles the intent for deletion of an event. To delete the correct event
        this steps are followed:
        1. Check if a title or date of the event, which is going to be deleted, is specified.
        2. If information is missing or the given information matches to multiple
        events the user is asked for more information to select a unique event that
        should be deleted.
        3. The user is asked for confirmation before an event is deleted finally
        :param message: the intent message
        :return none
        """
        event = self.select_event_for_altering(message)
        self.delete_event_on_confirmation(event)

    @intent_handler("rename.event.intent")
    def handle_rename_event(self, message):
        """
        Handles the intent for renaming an event. The correct event is selected
        based on given title or date. The event summary is changed to the new defined
        event title.
        :param message: the intent message
        :return: None
        """
        event = self.select_event_for_altering(message)
        self.rename_event(event)

    @intent_handler("create.event.intent")
    def handle_create_event(self, message):
        """
        Handler to create a new event in the calendar. It checked first
        if a title or date is given in the intent message. Then the user is
        asked for missing information as start time, duration or full-day event.
        If all information are present the event is created using the CalDav interface.
        :param message: the intent message
        :return: None
        """
        title, date = get_title_date_from_message(message)
        fullday = False
        while title is None:
            title = self.get_response("ask.for.title", {"action": "create"})
        self.log.info(f"set title of new event to: {title}")

        if date is None:
            date_response = self.get_response("ask.for.date")
            date, rest = extract_datetime(date_response)
        self.log.info(f"set date of new event to: {date}")

        extracted = extract_datetime(title, datetime.now(self.timezone))
        if extracted is not None:
            date_in_title, rest = extracted
            if date_in_title is not None:
                self.log.info("Event title included date")
                date_said = title.replace(rest, "")
                title = title.replace(date_said, "")

        if date.time() == dt.time(0):
            time, rest = None, None
            pattern = re.compile(r"full\s*day")
            while time is None or time.time() == dt.time(0):
                rest = self.get_response("new.event.starttime", {"event": title})
                extracted = extract_datetime(rest)
                if extracted is not None:
                    time, rest = extracted
                if re.search(pattern, rest):
                    fullday = True
                    break

            if not fullday:
                date = datetime.combine(date.date(), time.time())

        duration = None
        while duration is None:
            if not fullday:
                duration_utterance = self.get_response("ask.duration.new.event")
                duration, rest = extract_duration(duration_utterance)
            else:
                duration_utterance = self.get_response("ask.fullday.duration")
                duration = extract_number(duration_utterance)

        self.log.info(f"New calendar event will be created. Title: {title}, Date: {str(date)}")

        self.caldav_interface.create_new_event(title, date, duration, fullday)

    def select_event_for_altering(self, message):
        """
        Method that is used to select the correct event to
        rename/delete based on title and date information
        given in the intent message.
        If necessary the user is asked for more information to
        get the correct unique event.
        :param message: the intent message
        :return: the event that should be renamed/deleted as a python dict
        """
        event = None
        title, date = get_title_date_from_message(message)

        self.log.info(f"Received altering intent with {title} and {date}")
        if title is None and date is None:
            title = self.get_response("ask.for.title", {"action": "delete"})
        if date is not None:
            event = self.select_event_date_not_none(date)
        if title is not None:
            event = self.select_event_title_not_none(title)
        return event

    def select_event_title_not_none(self, title):
        """
        If just the title of an event that should be deleted is given this
        method is used to handle the selection of the correct event if there are
        multiple events containing the defined title string. When the event is
        found the user is asked for confirmation and the event is deleted.
        :param title: string that the event title needs to contain
        :return: None
        """
        events_matching_title = self.caldav_interface.get_events_with_title(title)
        if len(events_matching_title) == 0:
            self.speak_dialog("no.matching.event")
        if len(events_matching_title) == 1:
            return events_matching_title[0]
        if len(events_matching_title) > 1:
            selection = [f"{event['title']} " +
                         f"for {nice_date(event['starttime'])} " +
                         f"at {nice_time(event['starttime'])}"
                         for event in events_matching_title]
            self.speak_dialog("multiple.matching.events", {"detail": "title"})
            selected_event_details = self.ask_selection(
                selection, "event.selection.delete", None, 0.5
            )
            if selected_event_details is not None:
                event = events_matching_title[selection.index(selected_event_details)]
                return event
            self.speak_dialog("no.event.changed", {"action": "deleted"})
        return None

    def select_event_date_not_none(self, date):
        """
        If the date of an event that should be deleted is given this
        method is used to handle the selection of the correct event if there are
        multiple events for that date. When the event is
        found the user is asked for confirmation and the event is deleted.
        :param date: datetime of the event that should be deleted
        :return: None
        """
        events_on_date = self.caldav_interface.get_events_for_date(date)
        if len(events_on_date) == 0:
            self.speak_dialog("no.events.events.on.date", {"date": nice_date(date)})
        if len(events_on_date) == 1:
            return events_on_date[0]
        if len(events_on_date) > 1:
            title_of_events = [event["title"] for event in events_on_date]
            self.speak_dialog("multiple.matching.events", {"detail": "date"})
            title = self.ask_selection(title_of_events, "event.selection.delete", None, 0.7)
            event = next((event for event in events_on_date if event["title"] == title), None)
            return event
        return None

    def delete_event_on_confirmation(self, event):
        """
        Asks the user for confirmation before a event is deleted. If user confirms the
        event is deleted from the Nextcloud calendar.
        :param event: dictionary with the details of the event
        """
        if event is not None:
            confirm = self.ask_yesno(
                'confirm.delete.event',
                {"title": event["title"], "date": nice_date(event["starttime"])}
            )
            if confirm == "yes":
                self.caldav_interface.delete_event(event)
                self.speak_dialog(
                    "successful.delete.event",
                    {"title": event["title"], "date": nice_date(event["starttime"])}
                )
                return
        self.speak_dialog("no.event.changed", {"action": "deleted"})

    def rename_event(self, event):
        """
        Is called when a specific event for altering is found. The user is asked for a new title
        of the event and the event title is changed using the CalDav interface.
        :param event: a specific event in python dict representation
        :return: None
        """
        if event is not None:
            new_title = self.get_response("rename.desired.title", {"title": event['title']})
            if new_title is not None:
                self.caldav_interface.rename_event(event, new_title)
                self.speak_dialog("successful.rename.event", {"new_title": new_title})
                return
        self.speak_dialog("no.event.changed", {"action": "renamed"})


def create_skill():
    """
    Creates an instance of the skill class. Required from MycroftAI
    :return: instance of skill class
    """
    return NextcloudCalendar()
