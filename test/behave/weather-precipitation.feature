 @xfail
 Feature: Mycroft Weather Skill precipitation forecasts

  Scenario Outline: will it rain locally today, when it is expected
    Given an english speaking user
     And there is rain predicted for today
     When the user says "<rain locally today when expected>"
     Then "mycroft-weather" should reply with "rain is expected today."

  Examples: will it rain locally today when expected

    | rain locally today when expected |
    | will it rain today |
    | will it be rainy today |
    | should I bring an umbrella |
    | do I need an umbrella |
    | should I bring a rain coat |
    | do I need a rain jacket |
    | does it look like rain today |

  Scenario Outline: will it rain locally today, when it is not expected
    Given an english speaking user
     And there is no rain predicted for today
     When the user says "<rain locally today when not expected>"
     Then "mycroft-weather" should reply with "no rain is expected today."

  Examples: will it rain locally today when not expected

    | rain locally today when not expected |
    | will it rain today |
    | will it be rainy today |
    | should I bring an umbrella |
    | do I need an umbrella |
    | should I bring a rain coat |
    | do I need a rain jacket |
    | does it look like rain today |

  Scenario Outline: will it snow locally today, when it is expected
    Given an english speaking user
     And there is snow predicted for today
     When the user says "<snow locally today when expected>"
     Then "mycroft-weather" should reply with "snow is expected today."

  Examples: will it snow locally today when expected

    | snow locally today when expected |
    | will it snow today |
    | will it be snowy today |
    | does it look like snow today |

  Scenario Outline: Will it snow locally today, when it is not expected
    Given an english speaking user
     And there is no snow predicted for today
     When the user says "<snow locally today when not expected>"
     Then "mycroft-weather" should reply with "no snow is expected today."

  Examples: will it snow locally today when not expected

    | snow locally today when not expected |
    | will it snow today |
    | will it be snowy today |
    | does it look like snow today |

  Scenario Outline: Will it rain in a location today, when it is expected
    Given an english speaking user
     And there is rain predicted for today in a location
     When the user says "<rain in a location today when expected>"
     Then "mycroft-weather" should reply with "yes, expect rain in Kansas City Missouri today"

  Examples: will it rain in a location today when expected

    | rain in a location today when expected |
    | will it rain in Kansas city today |
    | is there a chance of rain in charleston south carolina today |
    | is there a chance of rain in paris |

  Scenario Outline: will it rain in a location in the future, when it is expected
    Given an english speaking user
     And there is rain predicted for the future in a location
     When the user says "<rain in a location in the future when expected>"
     Then "mycroft-weather" should reply with "yes, the forecast calls for light rain in charleston south carolina tomorrow"

  Examples: will it rain in a location in the future when expected

    | will it rain in charleston south carolina tomorrow |
    | will it rain in chicago on wednesday |
