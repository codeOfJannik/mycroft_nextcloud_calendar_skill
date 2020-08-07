Feature: create-appointment

  Scenario Outline: create appointment
    Given an english speaking user
    When the user says "<create an appointment>"
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to create?"
    And the user replies with "Test event"
    Then "nexcloud-calendar" should reply with dialog from "ask.for.date.dialog"
    And the user replies with "tomorrow at 1 pm"
    Then "nexcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"
    And the user replies with "1 hour"
    Then "nexcloud-calendar" should reply with dialog from "successful.create.event.dialog"

    Examples: Create an appointment
      | create an appointment |
      | create an event |
      | plan a new appointment |
      | add an event |