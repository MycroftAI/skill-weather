Feature: Mycroft Weather Skill location forecasts and temperature

  Scenario Outline: what is the current local weather in a location
    Given an english speaking user
     When the user says "<current weather in location>"
     Then "mycroft-weather" should reply with dialog from "Right now, it's overcast clouds and 32 degrees."

  Examples: what is the current local weather in a location

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

  Scenario Outline: what is the temperature today in location
    Given an english speaking user
     When the user says "<what is the temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "Right now, it's 34 degrees in new york"

  Examples: what is the temperature today in location

    | What is the temperature today in location |
    | temperature in sydney |
    | what's the temperature in new york city |
    | what will be the temperature today in berlin |
    | temperature today in san francisco, california |
    | temperature outside in kansas city |
    | In tokyo what's the temp |

  Scenario Outline: what is the high temperature today in location
    Given an english speaking user
     When the user says "<what is the high temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "A high of 38 degrees can be expected in new york"

  Examples: what is the high temperature today in location

    | what is the high temperature today in sydney |
    | high temperature in new york city |
    | what's the high temp today in berlin |
    | what's the high temperature in san francisco california |
    | how hot will it be today in kansas city |
    | how hot is it today in tokyo |
    | what's the current high temperature in kansas |

  Scenario Outline: what is the low temperature today in location
    Given an english speaking user
     When the user says "<what is the low temperature today in location>"
     Then "mycroft-weather" should reply with "Temperatures can be as low as 25 degrees in topeka"

  Examples: what is the low temperature today in location

    | what is the low temperature today in location |
    | what is the low temperature today in sydney |
    | low temperature in new york city |
    | what's the low temp today in berlin |
    | what's the low temperature in san francisco california |
    | how cold will it be today in kansas city |
    | how cold is it today in tokyo |
    | what's the current low temperature in kansas |

  Scenario Outline: What is the forecast for a future date in location
    Given an english speaking user
     When the user says "<what is the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "fThe forecast on tuesday is 49 for a high and 46 for a low in new york"

  Examples: what is the forecast for a future date in location

    | what is the forecast for a future date |
    | what is the weather tomorrow in sydney |
    | what is the weather like in new york city next tuesday |
    | what is the weather like in berline on sunday |
    | what is the weather like in san francisco california on saturday |
    | what is the weather like kansas city next friday |
