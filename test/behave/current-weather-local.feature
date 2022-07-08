Feature: Mycroft Weather Skill local current weather conditions

  Scenario Outline: What is the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog that includes "current-weather-local.dialog"

  Examples: What is the current local weather
    | current local weather |
    | tell me the current weather |
    | what's the current weather like |
    | what is the current weather like |
    | current weather |
    | what is it like outside |
    | what's the current weather conditions |
    | give me the current weather |
    | tell me the current weather |
    | how's the weather |
    | tell me the weather |
    | what's the weather like |
    | weather |
    | what's the weather conditions |
    | give me the weather |
    | tell me the weather |
    | what's the forecast |
    | weather forecast |
    | what's the weather forecast |
    | how is the weather now |
    | what is it like outside right now |
    | what's it like outside |
    | what's it like outside today |
