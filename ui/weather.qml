import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherDelegate {
    id: root

    spacing: proportionalGridUnit * 5

    LottieAnimation {
        id: weatherAnimation
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: Math.min(root.contentWidth, proportionalGridUnit * 50)
        Layout.preferredHeight: Layout.preferredWidth

        source: Qt.resolvedUrl(getWeatherImagery(sessionData.weathercode))

        loops: Animation.Infinite
        fillMode: Image.PreserveAspectFit
        running: true

        // Debug:
        onSourceChanged: {
            console.log(getWeatherImagery(sessionData.weathercode));
        }
        onStatusChanged: {
            console.log(weatherAnimation.status, errorString);
        }
    }

    Label {
        id: temperature
        font.weight: Font.Bold
        Layout.fillWidth: true
        horizontalAlignment: Text.AlignHCenter
        Layout.preferredHeight: proportionalGridUnit * 40
        font.pixelSize: parent.height * 0.65
        rightPadding: -font.pixelSize * 0.1
        text: sessionData.current + "°"
    }
}
