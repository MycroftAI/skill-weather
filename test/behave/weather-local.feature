Feature: mycroft-weather

  Scenario Outline: What's the current local weather
    Given an english speaking user
     When the user says "<current local weather>"
     Then "mycroft-weather" should reply with dialog from "Right now, it's overcast clouds and 32 degrees."

    | current local weather |
    | tell me the current weather |
    | how is the weather now |
    | what's the current weather like |
    | what is the current weather like |
    | current weather |
    | what is it like outside |
    | what is it like outside right now |
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

  Scenario Outline: What's the temperature today
    Given an english speaking user
     When the user says "<what is the temperature today>"
     Then "mycroft-weather" should reply with dialog from "it's currently 42 degrees"

    | What is the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |

  Scenario Outline: What's the high temperature today
    Given an english speaking user
     When the user says "<what is the high temperature today>"
     Then "mycroft-weather" should reply with dialog from "A high of 42 degrees can be expected"

    | what is the high temperature today |
    | high temperature |
    | what's the high temp today |
    | what's the high temperature |
    | how hot will it be today |
    | how hot is it today |
    | what's the current high temperature |

  Scenario Outline: What's the low temperature today
    Given an english speaking user
     When the user says "<what is the temperature today>"
     Then "mycroft-weather" should reply with dialog from "A low of 27 degrees can be expected"

    | What is the temperature today |
    | temperature |
    | what's the temperature |
    | what will be the temperature today |
    | temperature today |
    | temperature outside |
    | what's the temp |

  Scenario Outline: what is the forecast for tomorrow
    Given an english speaking user
     When the user says "<what is the forecast for tomorrow>"
     Then "mycroft-weather" should reply with dialog from "The forecast tomorrow is a high of 34 and a low of 23"

    | what is the forecast for tomorrow |
    | what is the weather tomorrow |
    | what is the weather like tomorrow |
    | tomorrow what will the weather be like |

  Scenario Outline: what is the forecast for a future date
    Given an english speaking user
     When the user says "<what is the forecast for a future date>"

    | what is the weather like next tuesday |
    | what is the weather like on saturday |
    | what is the weather like next monday |
    | what is the weather like in 9 days from now |

  Scenario Outline: What is the temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the temperature tomorrow>"
     Then "mycroft-weather" should reply with "tomorrow the temperature will be 31"

    | what is the temperature tomorrow |
    | what will be the temperature for tomorrow |
    | what's the temperature tomorrow |

  Scenario Outline: what is the high temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the high temperature tomorrow>"
     Then "mycroft-weather" should reply with "tomorrow it will be as high as 34"

    | what is the high temperature tomorrow |
    | tomorrow what is the high temperature |
    | what should I expect for a high temperature tomorrow |
    | what is the expected high temperature for tomorrow |
    | tomorrow how hot will it get |
    | how hot will it be tomorrow |

  Scenario Outline: what is the low temperature for tomorrow
    Given an english speaking user
     When the user says "<what is the low temperature tomorrow"
     Then "mycroft-weather" should reply with "tomorrow it will be as low as 23"

    | what is the low temperature tomorrow |
    | tomorrow what the low temperature |
    | what should I expect for a low temperature tomorrow |
    | what is the expected low temperature for tomorrow |
    | how cold will it be tomorrow |

  Scenario Outline: what is the temperature for a future date
    Given an english speaking user
     When the user says "<what is the temperature for a future date"
     Then "mycroft-weather" should reply with "on monday the temperature will be 40 degrees"

    | what is the temperature for a future date |
    | what is the temperature for wednesday |
    | what is the temperature for saturday |
    | what is the temperature 5 days from now |

  Scenario Outline: what is the high temperature for a future date
    Given an english speaking user
     When the user says "<what is the high temperature for a future date>"
     Then "mycroft-weather" should reply with "on saturday it will be as high as 53"

    | what is the high temperature for a future date |
    | what is the high temperature for wednesday |
    | what is the high temperature for saturday |
    | what is the high temperature 5 days from now |


  Scenario Outline: what is the low temperature for a future date
    Given an english speaking user
     When the user says "<what is the low temperature for a future date>"
     Then "mycroft-weather" should reply with "on saturday it will be as low as 30 degrees"

    | what is the low temperature for a future date |
    | what is the low temperature for wednesday |
    | what is the low temperature for saturday |
    | what is the low temperature 5 days from now |
