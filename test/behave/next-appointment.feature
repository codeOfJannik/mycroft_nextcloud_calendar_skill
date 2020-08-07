Feature: next-appointment

  Scenario Outline: next appointment
    Given an english speaking user
    When the user says <when is my next appointment>
    Then "nextcloud-calendar" should reply with anything
    And the reply should contain "appointment"

    Examples: When is my next appointment
      | when is my next appointment |
      | what is my next appointment |
      | when's my next appointment |
      | what's my next appointment |
      | when will my next appointment take place |