Feature: Mycroft Weather Skill local forecasted temperatures

  Scenario Outline: What is the temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-local.dialog"

  Examples: what is the temperature for tomorrow
    | what is the temperature tomorrow |
    | what will be the temperature for tomorrow |


  @xfail
  # Jira MS-98 https://mycroft.atlassian.net/browse/MS-98
  Scenario Outline: Failing what is the temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-local.dialog"

  Examples: what is the temperature for tomorrow
    | what is the temperature tomorrow |
    | what's the temperature tomorrow |


  Scenario Outline: what is the high temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the high temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-high-local.dialog"

  Examples: what is the high temperature for tomorrow
    | what is the high temperature tomorrow |
    | what is the high temperature tomorrow |
    | tomorrow what is the high temperature |
    | tomorrow how hot will it get |
    | how hot will it be tomorrow |
    | what should I expect for a high temperature tomorrow |
    | what is the expected high temperature for tomorrow |


  Scenario Outline: what is the low temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the low temperature tomorrow>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-low-local.dialog"

  Examples: what is the low temperature for tomorrow
    | what is the low temperature tomorrow |
    | what is the low temperature tomorrow |
    | tomorrow what is the low temperature |
    | how cold will it be tomorrow |
    | what should I expect for a low temperature tomorrow |
    | what is the expected low temperature for tomorrow |


  Scenario Outline: what is the temperature for a future date
    Given an english speaking user
     When the user says "<what is the temperature for a future date>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-local.dialog"

  Examples: what is the temperature for a future date
    | what is the temperature for a future date |
    | what is the temperature for wednesday |
    | what is the temperature for saturday |
    | what is the temperature 5 days from now |

  Scenario Outline: what is the high temperature for a future date
    Given an english speaking user
     When the user says "<what is the high temperature for a future date>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-high-local.dialog"

  Examples: what is the high temperature for a future date
    | what is the high temperature for a future date |
    | what is the high temperature for wednesday |
    | what is the high temperature for saturday |
    | what is the high temperature 5 days from now |

  Scenario Outline: what is the low temperature for a future date
    Given an english speaking user
     When the user says "<what is the low temperature for a future date>"
     Then "mycroft-weather" should reply with dialog that includes "daily-temperature-low-local.dialog"

  Examples: what is the low temperature for a future date
    | what is the low temperature for a future date |
    | what is the low temperature for wednesday |
    | what is the low temperature for saturday |
    | what is the low temperature 5 days from now |

  Scenario Outline: what is the temperature at a certain time
    Given an english speaking user
     When the user says "<what is the temperature at a certain time>"
     Then "mycroft-weather" should reply with dialog that includes "hourly-temperature-local.dialog"

  Examples: what is the temperature at a certain time
    | what is the temperature at a certain time |
    | what will the temperature be tonight |
    | what will the temperature be this evening |
    | what is the temperature this morning |

  @xfail
  Scenario Outline: Failing - what is the temperature at a certain time
    Given an english speaking user
     When the user says "<Failing what is the temperature at a certain time>"
     Then "mycroft-weather" should reply with dialog that includes "hourly-temperature-local.dialog"

  Examples: Failing what is the temperature at a certain time
    | Failing what is the temperature at a certain time |
    | temperature in the afternoon |
