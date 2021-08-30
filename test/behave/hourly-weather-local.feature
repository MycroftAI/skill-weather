Feature: Mycroft Weather Skill local hourly forecasts

  Scenario Outline: what is the weather later
    Given an english speaking user
     When the user says "<what is the weather later>"
     Then "mycroft-weather" should reply with dialog from "hourly-weather-local.dialog"

  Examples: What is the weather later
    | what is the weather later |
    | what is the weather later |

  @xfail
  Scenario Outline: Failing - what is the weather later
    Given an english speaking user
     When the user says "<failing - what is the weather later>"
     Then "mycroft-weather" should reply with dialog from "hourly-weather-local.dialog"

  Examples: Failing - What is the weather later
    | failing - what is the weather later |
    | what's the weather later today |
