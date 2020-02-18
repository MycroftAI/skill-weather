Feature: mycroft-weather

  Scenario Outline: What's the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog from "Right now, it's overcast clouds and 32 degrees."

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

  Scenario Outline: What's the temperature today
    Given an english speaking user
     When the user says "<what's the temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.temperature.dialog"

    | What's the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |

  Scenario Outline: What's the high temperature today
    Given an english speaking user
     When the user says "<what's the high temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.high.temperature.dialog"

    | what's the high temperature today |
    | high temperature |
    | what's the high temp today |
    | what's the high temperature |
    | how hot will it be today |
    | how hot is it today |
    | what's the current high temperature |

  Scenario Outline: What's the low temperature today
    Given an english speaking user
     When the user says "<what's the temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.low.temperature.dialog"

    | What's the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |

  Scenario Outline: What's the Forecast for a future date
    Given an english speaking user
     When the user says "<what's the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

    | what's the forecast for a future date |
    | what is the weather tomorrow |
    | what is the weather like next tuesday |
    | what is the weather like sunday |
    | what is the weather like saturday |
    | what is the weather like next friday |
