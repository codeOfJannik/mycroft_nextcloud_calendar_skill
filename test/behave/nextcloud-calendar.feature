# Created by jannik at 28.06.20
Feature: mycroft-nextcloud-calendar

  Scenario: number of appointments today
    Given an english speaking user
     When the user says "how many appointments do I have today"
     Then "mycroft-nextcloud-calendar" should reply with dialog from "number.appointments.today"

  Scenario: number of appointments on date
    Given an english speaking user
     When the user says "how many appointments do I have on"
     Then "mycroft-nextcloud-calendar" should reply with dialog from "number.appointments.on"

  Scenario: next appointment
    Given an english speaking user
     When the user says "when is my next appointment"
     Then "mycroft-nextcloud-calendar" should reply with dialog from "next.appointment.details"

  Scenario: appointment at time
    Given an english speaking user
     When the user says "do I have an appointment today at 1 pm"
     Then "mycroft-nextcloud-calendar" should reply with dialog from "specific.appointment.details"