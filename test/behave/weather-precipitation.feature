  Scenario Outline: local rain today expected
    Given an english speaking user
     And there is rain predicted for today
     When the user says "<local rain today when it is expected>"
     Then "mycroft-weather" should reply with "rain is expected today."

    | local rain today when it is expected |
    | will it rain today |
    | will it be rainy today |
    | should I bring an umbrella |
    | do I need an umbrella |
    | should I bring a rain coat |
    | do I need a rain jacket |
    | does it look like rain today |

  Scenario Outline: local rain today not expected
    Given an english speaking user
     And there is no rain predicted for today
     When the user says "<local rain today when it is not expected>"
     Then "mycroft-weather" should reply with "no rain is expected today."

    | local rain today when it is not expected |
    | will it rain today |
    | will it be rainy today |
    | should I bring an umbrella |
    | do I need an umbrella |
    | should I bring a rain coat |
    | do I need a rain jacket |
    | does it look like rain today |

  Scenario Outline: local snow today expected
    Given an english speaking user
     And there is rain predicted for today
     When the user says "<local snow today when it is expected>"
     Then "mycroft-weather" should reply with "snow is expected today."

    | local snow today when it is expected |
    | will it snow today |
    | will it be snowy today |
    | does it look like snow today |

  Scenario Outline: local snow today not expected
    Given an english speaking user
     And there is no rain predicted for today
     When the user says "<local snow today when it is not expected>"
     Then "mycroft-weather" should reply with "no snow is expected today."

    | local snow today when it is not expected |
    | will it snow today |
    | will it be snowy today |
    | does it look like snow today |
