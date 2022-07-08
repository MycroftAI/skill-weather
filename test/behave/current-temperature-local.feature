Feature: Mycroft Weather Skill current local weather

  Scenario Outline: What is the temperature today
    Given an english speaking user
     When the user says "<what is the temperature today>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-local.dialog"

  Examples: What is the temperature today
    | what is the temperature today |
    | what is the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | what's the temp |
    | temperature outside |


  Scenario Outline: What is the high temperature today
    Given an english speaking user
     When the user says "<what is the high temperature today>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-high-local.dialog"

  Examples: What is the high temperature today
    | what is the high temperature today |
    | what is the high temperature today |
    | what's the high temp today |
    | what's the high temperature |
    | how hot will it be today |
    | how hot is it today |
    | what's the current high temperature |
    | high temperature |


  Scenario Outline: What is the low temperature today
    Given an english speaking user
     When the user says "<what is the low temperature today>"
     Then "mycroft-weather" should reply with dialog that includes "current-temperature-low-local.dialog"

  Examples: What is the low temperature today
    | what is the low temperature today |
    | what is the low temperature today |
    | what will the lowest temperature be today |

