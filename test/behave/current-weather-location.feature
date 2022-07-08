Feature: Mycroft Weather Skill current weather at a specified location

  Scenario Outline: User asks for the current weather in a location
    Given an english speaking user
     When the user says "<what is the current weather in location>"
     Then "mycroft-weather" should reply with dialog that includes "current-weather-location.dialog"

  Examples: what is the current local weather in a location
    | what is the current weather in location |
    | what is the current weather in san francisco, california |
    | current weather in kansas city |
    | tell me the current weather in sydney |
    | what's the current weather like in berlin |
    | how's the weather in Paris |
    | tell me the weather in Paris, Texas |
    | give me the current weather in Kansas |
    | what is it like outside in italy |
    | In tokyo what is it like outside |
    | how is the weather in new york city |
    | what is it like outside in baltimore today |


  @xfail
  Scenario Outline: FAILING User asks for the current weather in a location
    Given an english speaking user
     When the user says "<what is the current weather in location>"
     Then "mycroft-weather" should reply with dialog that includes "current-weather-location.dialog"

  Examples: what is the current local weather in a location
    | what is the current weather in location |
    | what's the current weather conditions in Washington, D.C. |


  Scenario Outline: User asks for the current weather in an unknown location
    Given an english speaking user
     When the user says "<what is the current weather in location>"
     Then "mycroft-weather" should reply with dialog that includes "location-not-found.dialog"

  Examples: what is the current local weather in a location
    | what is the current weather in location |
    | tell me the current weather in Missouri |
