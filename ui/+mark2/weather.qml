import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import Qt.labs.lottieqt 1.0

WeatherDelegate {
    id: root

    spacing: proportionalGridUnit * 5
    
    Item {
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: Math.min(root.contentWidth, proportionalGridUnit * 50)
        Layout.preferredHeight: Layout.preferredWidth
        
        LottieAnimation {
            id: weatherAnimation
            source: Qt.resolvedUrl(getWeatherImagery(sessionData.weathercode))
            scale: Math.min(parent.height / height, parent.width / width)
            loops: LottieAnimation.Infinite
            autoPlay: true
        }
    }

    Mycroft.AutoFitLabel {
        id: temperature
        font.weight: Font.Bold
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        rightPadding: -font.pixelSize * 0.1
        text: sessionData.current + "°"
    }
}
