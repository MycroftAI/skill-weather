Feature: mycroft-weather

  Scenario: Forcast for today
    Given an english speaking user
     When the user says "what is the forecast"
     Then "mycroft-weather" should reply with dialog from "current.local.weather.dialog"

  Scenario: Temperature in paris
    Given an english speaking user
     When the user says "how hot will it be in paris"
     Then "mycroft-weather" should reply with dialog from "current.high.temperature.dialog"

  Scenario: Simple temperature
    Given an english speaking user
     When the user says "temperature"
     Then "mycroft-weather" should reply with dialog from "current.local.temperature.dialog"

  Scenario: Forecast for sunday
    Given an english speaking user
     When the user says "what's the forecast for sunday"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Scenario: Weather in Sidney tomorrow
    Given an english speaking user
     When the user says "what's the weather like in sydney tomorrow"
     Then "mycroft-weather" should reply with dialog from "forecast.weather.dialog"

  Scenario: temperature next saturday in auckland
    Given an english speaking user
     When the user says "next saturday how hot will it be in auckland"
     Then "mycroft-weather" should reply with dialog from "forecast.high.temperature.dialog"

  Scenario: Weather tomorrow
    Given an english speaking user
     When the user says "what is the weather tomorrow"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Scenario: What is the temperature
    Given an english speaking user
     When the user says "what's the temperature"
     Then "mycroft-weather" should reply with dialog from "current.local.temperature.dialog"

  Scenario: Temperature tonight
    Given an english speaking user
     When the user says "what will the temperature be tonight"
     Then "mycroft-weather" should reply with dialog from "at.time.local.temperature.dialog"

  Scenario: Temperature today
    Given an english speaking user
     When the user says "how hot is it today"
     Then "mycroft-weather" should reply with dialog from "current.local.high.temperature.dialog"

  Scenario: Sunset in perth
    Given an english speaking user
     When the user says "when does the sun set in perth"
     Then "mycroft-weather" should reply with dialog from "sunset.dialog"

  Scenario: cold temperature tomorrow
    Given an english speaking user
     When the user says "how cold will it get tomorrow"
     Then "mycroft-weather" should reply with dialog from "forecast.local.low.temperature.dialog"

  Scenario: Simple sunrise
    Given an english speaking user
     When the user says "when's the sunrise"
     Then "mycroft-weather" should reply with dialog from "sunrise.dialog"

  Scenario: Forcast for next tuesday
    Given an english speaking user
     When the user says "what's the forecast for next tuesday"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Scenario: Low temperature for today
    Given an english speaking user
     When the user says "what's the low today"
     Then "mycroft-weather" should reply with dialog from "current.local.low.temperature.dialog"

  Scenario: Sunrise in Paris
    Given an english speaking user
     When the user says "when does the sun rise in paris"
     Then "mycroft-weather" should reply with dialog from "sunrise.dialog"

  Scenario: Simple sunset
    Given an english speaking user
     When the user says "when's the sunset"
     Then "mycroft-weather" should reply with dialog from "sunset.dialog"

  Scenario Outline: current local weather question
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with "Right nowasdffh, it's overcast clouds and 32 degrees"

   Examples: local weather questions
     | current local weather |
     | tell me the current weather |
     | how is the weather now |
     | what's the current weather like |
     | what is the current weather like |
     | current weather |
     | what is it like outside |
     | what is it like outside right now |
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
