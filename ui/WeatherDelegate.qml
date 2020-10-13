import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.ProportionalDelegate {
    id: root

    function getWeatherImagery(weathercode) {
        switch(weathercode) {
        case 0:
            return "images/sunny.png";
            break
        case 1:
            return "images/partly_cloudy.png";
            break
        case 2:
            return "images/cloudy.png";
            break
        case 3:
            return "images/raining.png";
            break
        case 4:
            return "images/raining.png";
            break
        case 5:
            return "images/stormy.png";
            break
        case 6:
            return "images/snowing.png";
            break
        case 7:
            return "images/windy.png";
            break
        }
    }

}
