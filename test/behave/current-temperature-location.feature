Feature: Mycroft Weather Skill current temperature at specified location

  Scenario Outline: User asks for the temperature today in a location
    Given an english speaking user
     When the user says "<what is the temperature today in location>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-location.dialog"

  Examples: what is the temperature today in location
    | what is the temperature today in location |
    | temperature in sydney |
    | temperature today in san francisco, california |
    | temperature outside in kansas city |
    | In tokyo what's the temp |
    | what will be the temperature today in berlin |
    | what's the temperature in new york city |


  Scenario Outline: User asks for the high temperature today in a location
    Given an english speaking user
     When the user says "<what is the high temperature today in location>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-high-location.dialog"

    Examples: what is the high temperature today in location
    | what is the high temperature today in location |
    | what's the high temperature in san francisco california |
    | how hot will it be today in kansas city |
    | what's the current high temperature in kansas |
    | how hot is it today in tokyo |
    | what is the high temperature today in sydney |
    | what's the high temp today in berlin |
    | high temperature in new york city |


  Scenario Outline: User asks for the low temperature in a location
    Given an english speaking user
     When the user says "<what is the low temperature today in location>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-low-location.dialog"

  Examples: low temperature today in location
    | what is the low temperature today in location |
    | what's the low temperature in san francisco california |
    | how cold will it be today in kansas city |
    | low temperature today in sydney |
    | what's the low temp today in berlin |
    | what's the current low temperature in kansas |
    | how cold is it today in tokyo |
    | low temperature in new york city |
