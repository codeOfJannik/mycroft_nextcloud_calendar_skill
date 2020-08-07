Feature: create-appointment-title-date

Scenario Outline: create appointment title date
    Given an english speaking user
    When the user says "<create an appointment entitled Test event tomorrow>"
    Then "nextcloud-calendar" should reply with dialog from "new.event.starttime.dialog"
    And the user replies with "9 am"
    Then "nexcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"
    And the user replies with "1 hour"
    Then "nexcloud-calendar" should reply with dialog from "successful.create.event.dialog"

    Examples: Create an appointment entitled Test event
      | create an appointment entitled Test event tomorrow |
      | create an event Test event on next monday |
      | plan a new appointment entitled Test event for the 1st of December |
      | add an event Test event for today |