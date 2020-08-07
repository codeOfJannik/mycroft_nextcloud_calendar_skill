Feature: create-appointment

  Scenario Outline: create appointment
    Given an english speaking user
    When the user says <create an appointment>
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to create?"

    Examples: Create an appointment
      | create an appointment |
      | create an event |
      | plan a new appointment |
      | add an event |

  Scenario Outline: create appointment on date
    Given an english speaking user
    When the user says <create an appointment for tomorrow 1 pm>
    Then "nextcloud-calendar" should reply with exactly "What is the title of the event you want to create?"

    Examples: Create an create an appointment for tomorrow 1 pm
      | create an appointment for tomorrow 1 pm |
      | create an event on next monday |
      | plan a new appointment for the 1st of December |
      | add an event today at 8 pm |

  Scenario Outline: create appointment title
    Given an english speaking user
    When the user says <create an appointment entitled Test event>
    Then "nextcloud-calendar" should reply with dialog from "ask.for.date.dialog"

    Examples: Create an appointment entitled Test event
      | create an appointment entitled Test event |
      | create an event Test event |
      | plan a new appointment entitled Test event |
      | add an event Test event |

  Scenario Outline: create appointment title date
    Given an english speaking user
    When the user says <create an appointment entitled Test event tomorrow>
    Then "nextcloud-calendar" should reply with dialog from "new.event.starttime.dialog"

    Examples: Create an appointment entitled Test event
      | create an appointment entitled Test event tomorrow |
      | create an event Test event on next monday |
      | plan a new appointment entitled Test event for the 1st of December|
      | add an event Test event today |

  Scenario Outline: create appointment title date time
    Given an english speaking user
    When the user says <create an appointment entitled Test event tomorrow at 9 am>
    Then "nextcloud-calendar" should reply with dialog from "ask.duration.new.event.dialog"

    Examples: Create an appointment entitled Test event
      | create an appointment entitled Test event tomorrow at 9 am |
      | create an event Test event on next monday in the evening |
      | plan a new appointment entitled Test event for the 1st of December 3 pm|
      | add an event Test event today afternoon|