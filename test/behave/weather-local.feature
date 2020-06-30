Feature: Mycroft Weather Skill local forecasts and temperature

  Scenario Outline: What is the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog from "current.local.weather.dialog"

  Examples: What is the current local weather
    | current local weather |
    | tell me the current weather |
    | what's the current weather like |
    | what is the current weather like |
    | current weather |
    | what is it like outside |
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

  @xfail
  # JIra MS-54 https://mycroft.atlassian.net/browse/MS-54
  Scenario Outline: Failing what is the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog from "current.local.weather.dialog"

  Examples: What is the current local weather
    | current local weather |
    | how is the weather now |
    | what is it like outside right now |

  Scenario Outline: What is the temperature today
    Given an english speaking user
     When the user says "<what is the temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.temperature.dialog"

  Examples: What is the temperature today
    | what is the temperature today |
    | what is the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |


  @xfail
  # JIra MS-55 https://mycroft.atlassian.net/browse/MS-55
  Scenario Outline: Failing What is the temperature today
    Given an english speaking user
     When the user says "<what is the temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.temperature.dialog"

  Examples: Failing temperature examples
    | what is the temperature today |
    | what's the temp |
    | temperature outside |

  Scenario Outline: What is the high temperature today
    Given an english speaking user
     When the user says "<what is the high temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.high.temperature.dialog"

  Examples: What is the high temperature today
    | what is the high temperature today |
    | what is the high temperature today |
    | what's the high temp today |
    | what's the high temperature |
    | how hot will it be today |
    | how hot is it today |
    | what's the current high temperature |

  @xfail
    # JIra MS-97 https://mycroft.atlassian.net/browse/MS-97
  Scenario Outline: Failing what is the high temperature today
    Given an english speaking user
     When the user says "<what is the high temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.high.temperature.dialog"

  Examples: What is the high temperature today
    | what is the high temperature today |
    | high temperature |

  Scenario Outline: What is the low temperature today
    Given an english speaking user
     When the user says "<what is the low temperature today>"
     Then "mycroft-weather" should reply with dialog from "current.local.low.temperature.dialog"

  Examples: What is the low temperature today
    | what is the low temperature today |
    | what is the low temperature today |
    | what will the lowest temperature be today |

  Scenario Outline: what is the forecast for tomorrow
    Given an english speaking user
     When the user says "<what is the forecast for tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Examples: What is the forecast for tomorrow
    | what is the forecast for tomorrow |
    | what is the forecast for tomorrow |
    | what is the weather tomorrow |
    | what is the weather like tomorrow |
    | tomorrow what will the weather be like |

  Scenario Outline: what is the forecast for a future date
    Given an english speaking user
     When the user says "<what is the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Examples: what is the forecast for a future date
    | what is the forecast for a future date |
    | what is the weather like next tuesday |
    | what is the weather like on next saturday |
    | what is the weather like next monday |

  @xfail
  # Jira MS-57 https://mycroft.atlassian.net/browse/MS-57
  Scenario Outline: failing what is the forecast for a future date
    Given an english speaking user
     When the user says "<what is the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

  Examples: what is the forecast for a future date
    | what is the forecast for a future date |
    | what is the weather like in 9 days from now |

  @xfail
  # Jira MS-98 https://mycroft.atlassian.net/browse/MS-98
  Scenario Outline: What is the temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.temperature.dialog"

  Examples: what is the temperature for tomorrow
    | what is the temperature tomorrow |
    | what will be the temperature for tomorrow |
    | what's the temperature tomorrow |

  Scenario Outline: what is the high temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the high temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.high.temperature.dialog"

  Examples: what is the high temperature for tomorrow
    | what is the high temperature tomorrow |
    | what is the high temperature tomorrow |
    | tomorrow what is the high temperature |
    | tomorrow how hot will it get |
    | how hot will it be tomorrow |

  @xfail
  # Jira Ms-98 https://mycroft.atlassian.net/browse/MS-98
  Scenario Outline: failing what is the high temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the high temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.high.temperature.dialog"

  Examples: what is the high temperature for tomorrow
    | what is the high temperature tomorrow |
    | what should I expect for a high temperature tomorrow |
    | what is the expected high temperature for tomorrow |

  Scenario Outline: what is the low temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the low temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.low.temperature.dialog"

  Examples: what is the low temperature for tomorrow
    | what is the low temperature tomorrow |
    | what is the low temperature tomorrow |
    | tomorrow what is the low temperature |
    | how cold will it be tomorrow |

  @xfail
  # Jira Ms-99 https://mycroft.atlassian.net/browse/MS-99
  Scenario Outline: failing what is the low temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the low temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.low.temperature.dialog"

  Examples: what is the low temperature for tomorrow
    | what is the low temperature tomorrow |
    | what should I expect for a low temperature tomorrow |
    | what is the expected low temperature for tomorrow |

  Scenario Outline: what is the temperature for a future date
    Given an english speaking user
     When the user says "<what is the temperature for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.temperature.dialog"

  Examples: what is the temperature for a future date
    | what is the temperature for a future date |
    | what is the temperature for next wednesday |
    | what is the temperature for next saturday |
    | what is the temperature 5 days from now |

  Scenario Outline: what is the high temperature for a future date
    Given an english speaking user
     When the user says "<what is the high temperature for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.high.temperature.dialog"

  Examples: what is the high temperature for a future date
    | what is the high temperature for a future date |
    | what is the high temperature for next wednesday |
    | what is the high temperature for next saturday |
    | what is the high temperature 5 days from now |

  Scenario Outline: what is the low temperature for a future date
    Given an english speaking user
     When the user says "<what is the low temperature for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.low.temperature.dialog"

  Examples: what is the low temperature for a future date
    | what is the low temperature for a future date |
    | what is the low temperature for next wednesday |
    | what is the low temperature for next saturday |
    | what is the low temperature 5 days from now |
