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
   | what's the current weather conditions in Washington DC |
   | give me the current weather in Kansas |
   | tell me the current weather Missouri |
   | how's the weather in Paris |
   | tell me the weather in Paris, Texas |

  Scenario Outline: What's the temperature today in Location
    Given an english speaking user
     When the user says "<what's the temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.temperature.dialog"

    | What's the temperature today in location |
    | temperature in sydney |
    | what's the temperature in new york city |
    | what will be the temperature today in berlin |
    | temperature today in san francisco, california |
    | temperature outside in kansas city |
    | In tokyo what's the temp |

  Scenario Outline: What's the high temperature today in location
    Given an english speaking user
     When the user says "<what's the high temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.high.temperature.dialog"

    | what's the high temperature today in sydney |
    | high temperature in new york city |
    | what's the high temp today in berlin |
    | what's the high temperature in san francisco california |
    | how hot will it be today |
    | how hot is it today |
    | what's the current high temperature |

  Scenario Outline: What's the low temperature today in location
    Given an english speaking user
     When the user says "<what's the temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.low.temperature.dialog"

    | What's the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |

  Scenario Outline: What's the Forecast for a future date in location
    Given an english speaking user
     When the user says "<what's the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

    | what's the forecast for a future date |
    | what is the weather tomorrow in sydney |
    | what is the weather like in new york city next tuesday |
    | what is the weather like in berline on sunday |
    | what is the weather like in san francisco california on saturday |
    | what is the weather like kansas city next friday |
