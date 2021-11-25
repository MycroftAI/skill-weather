Feature: Mycroft Weather Skill current local humidity

  Scenario Outline: What is the humidity today
    Given an english speaking user
     When the user says "<what is the humidity today>"
     Then "mycroft-weather" should reply with dialog from "current-humidity-local.dialog"

  Examples: What is the humidity today
    | what is the humidity today |
    | what is the humidity today |
    | what's the humidity |
    | what will be the humidity today |
    | how humid is it |
    | how humid is it outside |

