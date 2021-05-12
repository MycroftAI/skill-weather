import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.ProportionalDelegate {
    id: root
    skillBackgroundColorOverlay: Qt.rgba(0, 0, 0, 1)

    function getWeatherImagery(weathercode) {
        switch(weathercode) {
        case 0:
            return "animations/sunny.json";
            break
        case 1:
            return "animations/partlycloudy.json";
            break
        case 2:
            return "animations/cloudy.json";
            break
        case 3:
            return "animations/rain.json";
            break
        case 4:
            return "animations/rain.json";
            break
        case 5:
            return "animations/storm.json";
            break
        case 6:
            return "animations/snow.json";
            break
        case 7:
            return "animations/fog.json";
            break
        }
    }

}
