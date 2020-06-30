# Created by jannik at 28.06.20
Feature: nextcloud-calendar

  Scenario: number of appointments today
    Given an english speaking user
     When the user says <number of appointments today>
     Then "nextcloud-calendar" should reply with dialog from "number.appointments.today.dialog"

  Examples: How many appointments do I have today
    | number of appointments today |
    | how many appointments do I have today |
    | many appointments today |
    | today's number of appointments |
    | today's appointments count |


  Scenario: number of appointments on a specific day
    Given an english speaking user
     When the user says <number of appointments tomorrow>
     Then "nextcloud-calendar" should reply with dialog from "number.appointments.specific.day.dialog"

  Examples: How many appointments do I have on my birthday
    | number of appointments tomorrow |
    | how many appointments do I have on Christmas Eve |
    | many appointments on my birthday |


  Scenario: number of appointments on date
    Given an english speaking user
     When the user says <number of appointments on first of June>
     Then "nextcloud-calendar" should reply with dialog from "number.appointments.on.dialog"

  Examples: How many appointments do I have on next Monday
    | number of appointments on first of June |
    | how many appointments do I have on next Monday |
    | how many appointments do I have next Monday |
    | many appointments on last Friday in August |
    | next Saturday's number of appointments |


  Scenario: next appointment
    Given an english speaking user
     When the user says <when is my next appointment>
     Then "nextcloud-calendar" should reply with dialog from "next.appointment.details.dialog"

  Examples: When is my next appointment
    | when is my next appointment |
    | what is my next appointment |
    | when's my next appointment |
    | what's my next appointment |
    | when will my next appointment take place |


  Scenario: appointment at datetime
    Given an english speaking user
     When the user says <do I have an appointment today at 1 pm>
     Then "nextcloud-calendar" should reply with dialog from "requested.time.appointment.details.dialog"

  Examples: Do I have an appointment at 1 pm today
    | do I have an appointment at 1 pm today |
    | do I have an appointment tomorrow at 10 am |
    | is there an appointment next week on Wednesday at 8 am |


  Scenario: no appointment at datetime
    Given an english speaking user
     When the user says <do I have an appointment today at 1 pm>
     Then "nextcloud-calendar" should reply with dialog from "requested.time.no.appointment.dialog"

  Examples: Do I have an appointment at 1 pm today
    | do I have an appointment at 1 pm today |
    | do I have an appointment tomorrow at 10 am |
    | is there an appointment next week on Wednesday at 8 am |


  Scenario: create new appointment
    Given an english speaking user
     When the user says <create an appointment>
     Then "nextcloud-calendar" should reply with dialog from "when.create.appointment.dialog"

  Examples: Create a new appointment
    | create an appointment |
    | create new appointment |
    | create a new appointment |
    | add a new appointment to my calendar |
    | new appointment |
    | create appointment |
    | plan new appointment |
    | plan a new appointment |
    | plan an appointment |


  Scenario: create new appointment with datetime
    Given an english speaking user
     When the user says <create an appointment today at 4 pm>
     Then "nextcloud-calendar" should reply with dialog from "what.title.create.appointment.dialog"

  Example: Create a new appointment today at 4 pm
    | create an appointment today at 4 pm |
    | new appointment tomorrow at 9 am |
    | plan a new appointment for 1st June at 7 pm |
    | schedule a meeting on next Wednesday at 1 pm |


  Scenario: create new appointment with title
    Given an english speaking user
     When the user says <create an appointment titled Speech Interaction class>
     Then "nextcloud-calendar" should reply with dialog from "what.datetime.create.appointment.dialog"

  Example: Create a new appointment titled Speech Interaction class
    | create an appointment titled Speech Interaction class |
    | create a new appointment for Playing Tennis |
    | schedule a meeting with Barack Obama |


  Scenario: create new appointment with details
    Given an english speaking user
     When the user says <create an appointment titled Speech Interaction class on next Monday at 4 pm>
     Then "nextcloud-calendar" should reply with dialog from "appointment.created.dialog"

  Example: Create a new appointment titled Speech Interaction class on next Monday at 4 pm
    | create an appointment titled Speech Interaction class on next Monday at 4 pm |
    | create a new appointment for Playing Tennis on August 13th at 7pm |
    | schedule a meeting with Barack Obama on Thanksgiving at lunch time |

  Scenario: cancel specific appointment
    Given an english speaking user
     When the user says <cancel Speech Interaction class on next Monday>
     Then "nextcloud-calendar" should reply with dialog from "cancel.specific.appointment.request.confirmation"

  Example: Cancel Speech Interaction class on next Monday
    | cancel Speech Interaction class on next Monday |
    | cancel my appointment on next Wednesday 3 pm |
    | delete my next appointment |


  Scenario: cancel all appointments in time period
    Given an english speaking user
     When the user says <cancel all appointments on next Monday>
     Then "nextcloud-calendar" should reply with dialog from "cancel.time.appointment.request.confirmation"

  Example: Cancel all appointments on next Monday
    | cancel all appointments on next Monday |
    | cancel my appointments on next Wednesday |
    | cancel all appointments scheduled for next week |
    | delete all appointments in June |