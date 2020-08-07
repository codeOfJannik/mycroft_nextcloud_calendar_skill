Feature: appointments-date

  Scenario Outline: date appointments
    Given an english speaking user
    When the user says "<do i have an appointment tomorrow>"
    Then "nextcloud-calendar" should reply with anything
    Then mycroft reply should contain "for"
    Then mycroft reply should contain "in your calendar"

    Examples: Do i have an appointment tomorrow
      | do i have an appointment tomorrow |
      | do i have an event on friday |
      | do i have appointments in two days |
      | do i have events on next wednesday |
      | are there appointments on 1st of december |
      | are there any events planned for saturday |
