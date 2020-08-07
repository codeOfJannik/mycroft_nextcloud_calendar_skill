Feature: rename-appointment

  Scenario Outline: rename appointment
    Given an english speaking user
    When the user says "<rename an event>"
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to rename?"
    And the user replies with "cancel"

    Examples: Rename an event
      | rename an event |
      | rename an appointment |
