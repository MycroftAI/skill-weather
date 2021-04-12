import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    id: root
    bottomPadding: 32
    leftPadding: 32
    rightPadding: 32
    topPadding: 32

    function getWeatherImagery(weathercode) {
        switch(weathercode) {
        case 0:
            return "images/sunny.svg";
            break
        case 1:
            return "images/partly_cloudy.svg";
            break
        case 2:
            return "images/cloudy.svg";
            break
        case 3:
            return "images/rain.svg";
            break
        case 4:
            return "images/rain.svg";
            break
        case 5:
            return "images/storm.svg";
            break
        case 6:
            return "images/snow.svg";
            break
        case 7:
            return "images/cloudy.svg";
            break
        }
    }

}
