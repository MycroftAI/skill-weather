@crash
Feature: Mycroft Weather Skill local current weather conditions

  Scenario Outline: What is the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog from "current-weather-local.dialog"

  Examples: What is the current local weather
    | current local weather |
    | tell me the current weather |
    | what's the current weather like |
    | what is the current weather like |
    | current weather |
