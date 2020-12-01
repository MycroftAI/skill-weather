import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import Qt.labs.lottieqt 1.0

WeatherDelegate {
    id: root

    property alias model: forecastRepeater.model
    property var fick: proportionalGridUnit * 1
    spacing: proportionalGridUnit * 10
    
    Repeater {
        id: forecastRepeater
        model: sessionData.forecast.first
        delegate: GridLayout {
            columns: 2
            rowSpacing: proportionalGridUnit * 5
            columnSpacing: proportionalGridUnit * 5
            Layout.fillWidth: true
            Item {
                Layout.alignment: Qt.AlignCenter
                Layout.preferredHeight: proportionalGridUnit * 20
                Layout.preferredWidth: Layout.preferredHeight                
                color: "transparent"
                
                LottieAnimation {
                    anchors.centerIn: parent
                    source: Qt.resolvedUrl(getWeatherImagery(modelData.weathercode))
                    loops: LottieAnimation.Infinite
                    scale: Math.min(parent.height / height, parent.width / width)
                    autoPlay: true
                }
            }
            Mycroft.AutoFitLabel {
                id: firstLabel
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 15
                text: modelData.date
            }

            Mycroft.AutoFitLabel {
                font.weight: Font.Bold
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 20
                rightPadding: -font.pixelSize * 0.1
                text: modelData.max + "°"
            }

            Mycroft.AutoFitLabel {
                font.styleName: "Thin"
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 20
                rightPadding: -font.pixelSize * 0.1
                text: modelData.min + "°"
            }
        }
    }
}
