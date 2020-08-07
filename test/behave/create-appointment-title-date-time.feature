Feature: create-appointment-title-date-time

Scenario Outline: create appointment title date time
    Given an english speaking user
    When the user says "<create an appointment entitled Test event tomorrow at 9 am>"
    Then "nextcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"
    And the user replies with "1 hour"
    Then "nexcloud-calendar" should reply with dialog from "successful.create.event.dialog"

    Examples: Create an appointment entitled Test event tomorrow at 9 am
      | create an appointment entitled Test event tomorrow at 9 am |
      | create an event Test event on next monday in the evening |
      | plan a new appointment entitled Test event for the 1st of December at 3 pm |
      | add an event Test event for today afternoon |