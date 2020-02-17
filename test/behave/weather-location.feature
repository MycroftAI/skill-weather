Feature: mycroft-weather

  Scenario Outline: What's the current local weather in a location
    Given an english speaking user
     When the user says "<current weather in location>"
     Then "mycroft-weather" should reply with dialog from "Right now, it's overcast clouds and 32 degrees."

   | current weather in location |
   | tell me the current weather in sydney |
   | how is the weather in new york city |
   | what's the current weather like in berlin |
   | what is the current weather in san francisco, california |
   | current weather in kansas city |
   | In tokyo what is it like outside |
   | what is it like outside in italy |
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
     Then "mycroft-weather" should reply with dialog from "current.local.weather.dialog"

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
     Then "mycroft-weather" should reply with dialog from "current.local.low.weather.dialog"

    | What's the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |
