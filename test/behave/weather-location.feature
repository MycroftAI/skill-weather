Feature: Mycroft Weather Skill location forecasts and temperature

  Scenario Outline: User asks for the current weather in a location
    Given an english speaking user
     When the user says "<what is the current weather in location>"
     Then "mycroft-weather" should reply with dialog from "current.weather.dialog"

  Examples: what is the current local weather in a location
    | what is the current weather in location |
    | how is the weather in new york city |
    | what is the current weather in san francisco, california |
    | current weather in kansas city |
    | what's the current weather conditions in Washington DC |

  @xfail
  Scenario Outline: Failing User asks for the current weather in a location
    Given an english speaking user
     When the user says "<what is the current weather in location>"
     Then "mycroft-weather" should reply with dialog from "current.weather.dialog"

  Examples: what is the current local weather in a location
    | what is the current weather in location |
    | what is it like outside in italy |
    | In tokyo what is it like outside |
    | give me the current weather in Kansas |
    | tell me the current weather Missouri |
    | tell me the current weather in sydney |
    | what's the current weather like in berlin |
    | how's the weather in Paris |
    | tell me the weather in Paris, Texas |

  Scenario Outline: User asks for the temperature today in location
    Given an english speaking user
     When the user says "<what is the temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.temperature.dialog"

  Examples: what is the temperature today in location
    | what is the temperature today in location |
    | what's the temperature in new york city |
    | what will be the temperature today in berlin |

  @xfail
  Scenario Outline: Failing user asks for the temperature today in location
    Given an english speaking user
     When the user says "<what is the temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.temperature.dialog"

  Examples: what is the temperature today in location
    | what is the temperature today in location |
    | temperature in sydney |
    | temperature today in san francisco, california |
    | temperature outside in kansas city |
    | In tokyo what's the temp |

  Scenario Outline: User asks for the high temperature today in a location
    Given an english speaking user
     When the user says "<what is the high temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.high.temperature.dialog"

    Examples: what is the high temperature today in location
    | what is the high temperature today in location |
    | what's the high temperature in san francisco california |
    | how hot will it be today in kansas city |

  @xfail
  Scenario Outline: Failing user asks for the high temperature today in a location
    Given an english speaking user
     When the user says "<what is the high temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.high.temperature.dialog"

    Examples: what is the high temperature today in location
    | what is the high temperature today in location |
    | high temperature in new york city |
    | what's the current high temperature in kansas |
    | how hot is it today in tokyo |
    | what is the high temperature today in sydney |
    | what's the high temp today in berlin |

  Scenario Outline: User asks for the low temperature in a location
    Given an english speaking user
     When the user says "<what is the low temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.low.temperature.dialog"

  Examples: low temperature today in location
    | what is the low temperature today in location |
    | what's the low temperature in san francisco california |
    | how cold will it be today in kansas city |

    @xfail
    Scenario Outline: Failing user asks for the low temperature in a location
    Given an english speaking user
     When the user says "<what is the low temperature today in location>"
     Then "mycroft-weather" should reply with dialog from "current.low.temperature.dialog"

  Examples: low temperature today in location
    | what is the low temperature today in location |
    | what is the low temperature today in sydney |
    | what's the low temp today in berlin |
    | what's the current low temperature in kansas |
    | low temperature in new york city |
    | how cold is it today in tokyo |

  Scenario Outline: User asks for the forecast on a future date in a location
    Given an english speaking user
     When the user says "<what is the forecast on a future date in a location>"
     Then "mycroft-weather" should reply with dialog from "forecast.weather.dialog"

  Examples: what is the forecast for a future date in location
    | what is the forecast on a future date in a location |
    | what is the weather tomorrow in sydney |
    | what is the weather like in new york city next tuesday |
    | what is the weather like in san francisco california next saturday |
    | what is the weather like in kansas city next friday |

  @xfail
  Scenario Outline: Failing User asks for the forecast on a future date in a location
    Given an english speaking user
     When the user says "<what is the forecast on a future date in a location>"
     Then "mycroft-weather" should reply with dialog from "forecast.weather.dialog"

  Examples: what is the forecast for a future date in location
    | what is the forecast on a future date in a location |
    | what is the weather like in berlin on sunday |
