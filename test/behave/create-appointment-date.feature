Feature: create-appointment-date

Scenario Outline: create appointment date
    Given an english speaking user
    When the user says "<create an appointment for tomorrow 1 pm>"
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to create?"
    And the user replies with "Test event"
    Then "nextcloud-calendar" should reply with dialog from "new.event.starttime.dialog"
    And the user replies with "9 am"
    Then "nexcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"
    And the user replies with "1 hour"
    Then "nexcloud-calendar" should reply with dialog from "successful.create.event.dialog"

    Examples: Create an create an appointment for tomorrow 1 pm
      | create an appointment for tomorrow 1 pm |
      | create an event on next monday |
      | plan a new appointment for the 1st of December |
      | add an event for today |