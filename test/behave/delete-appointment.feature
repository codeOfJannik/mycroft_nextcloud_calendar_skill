Feature: delete-appointment

  Scenario Outline: delete appointment
    Given an english speaking user
    When the user says <delete an appointment>
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to delete?"

    Examples: Delete an appointment
      | delete an appointment |
      | delete an event |