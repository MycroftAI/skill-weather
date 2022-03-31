Feature: Mycroft Weather Skill daily forecast for a specified location.

  Scenario Outline: User asks for the forecast on a future date in a location
    Given an english speaking user
     When the user says "<what is the forecast on a future date in a location>"
     Then "mycroft-weather" should reply with dialog that includes "daily-weather-location.dialog"

  Examples: what is the forecast for a future date in location
    | what is the forecast on a future date in a location |
    | what is the weather tomorrow in sydney |
    | what is the weather like in new york city tuesday |
    | what is the weather like in san francisco california saturday |
    | what is the weather like in kansas city friday |
    | what is the weather like in berlin on sunday |
