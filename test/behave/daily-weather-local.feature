Feature: Mycroft Weather Skill local daily forecasts

  Scenario Outline: what is the forecast for tomorrow
    Given an english speaking user
     When the user says "<what is the forecast for tomorrow>"
     Then "mycroft-weather" should reply with dialog that includes "daily-weather-local.dialog"

  Examples: What is the forecast for tomorrow
    | what is the forecast for tomorrow |
    | what is the forecast for tomorrow |
    | what is the weather tomorrow |
    | what is the weather like tomorrow |
    | tomorrow what will the weather be like |

  Scenario Outline: what is the forecast for a future date
    Given an english speaking user
     When the user says "<what is the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog that includes "daily-weather-local.dialog"

  Examples: what is the forecast for a future date
    | what is the forecast for a future date |
    | what is the weather like tuesday |
    | what is the weather like on saturday |
    | what is the weather like monday |
    | what is the weather like 5 days from now |

  Scenario Outline: multiple day forecast
    Given an english speaking user
     When the user says "<multiple day forecast request>"
     Then "mycroft-weather" should reply with dialog that includes "daily-weather-local.dialog"
    #  Single utterance being used for MVP
    #  Then "mycroft-weather" should reply with dialog that includes "daily-weather-local.dialog"
    #  Then "mycroft-weather" should reply with dialog that includes "daily-weather-local.dialog"

  Examples: what is the forecast for a future date
    | multiple day forecast request |
    | what is the forecast for the next three days |
    | what is the weather forecast for the next three days |
    | what is the three-day weather forecast |
    | for the next three days what is the weather forecast |
