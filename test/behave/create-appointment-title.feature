Feature: create-appointment-title

  Scenario Outline: create appointment title
    Given an english speaking user
    When the user says "<create an appointment entitled Test event>"
    Then "nextcloud-calendar" should reply with dialog from "ask.for.date.dialog"
    And the user replies with "tomorrow at 5 pm"
    Then "nexcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"
    And the user replies with "1 hour"
    Then "nexcloud-calendar" should reply with dialog from "successful.create.event.dialog"

    Examples: Create an appointment entitled Test event
      | create an appointment entitled Test event |
      | create an event Test event |
      | plan a new appointment entitled Test event |
      | add an event Test event |