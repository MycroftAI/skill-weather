  Scenario Outline: What's the Forecast for a future date
    Given an english speaking user
     When the user says "<what's the forecast for a future date>"
     Then "mycroft-weather" should reply with dialog from "forecast.local.weather.dialog"

    | what's the forecast for a future date |
    | what is the weather tomorrow |
    | what is the weather like next tuesday |
    | what is the weather like sunday |
    | what is the weather like saturday |
    | what is the weather like next friday |
    
