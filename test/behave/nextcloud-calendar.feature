# Created by jannik at 28.06.20
Feature: nextcloud-calendar

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