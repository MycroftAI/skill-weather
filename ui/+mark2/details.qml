import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import Qt.labs.lottieqt 1.0

WeatherDelegate {
    id: root

    spacing: proportionalGridUnit
    Mycroft.AutoFitLabel {
        wrapMode: Text.WordWrap
        text: sessionData.location
        lineHeight: 0.6
        horizontalAlignment: Layout.alignLeft
        Layout.alignment: Qt.AlignLeft
        Layout.preferredHeight: proportionalGridUnit * 15
        Layout.preferredWidth : 300
    }
    Item {
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: Math.min(root.contentWidth, proportionalGridUnit * 40)
        Layout.preferredHeight: Layout.preferredWidth
        
        LottieAnimation {
            id: weatherAnimation
            source: Qt.resolvedUrl(getWeatherImagery(sessionData.weathercode))
            scale: Math.min(parent.height / height, parent.width / width)
            loops: LottieAnimation.Infinite
            autoPlay: true
        }
    }
    GridLayout {
        columns: 2
        columnSpacing: proportionalGridUnit * 5
        rowSpacing: proportionalGridUnit * 5
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: Math.min(root.contentWidth, proportionalGridUnit * 50)
        
        ColumnLayout {
            Mycroft.AutoFitLabel {
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 3
                text: "Min:"
            }
            Mycroft.AutoFitLabel {
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 15
                text: sessionData.min + "°"
            }
        }
        
        ColumnLayout {
            Mycroft.AutoFitLabel {
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 3
                text: "Max:"
            }
            Mycroft.AutoFitLabel {
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 15
                text: sessionData.max + "°"
            }
        }
        ColumnLayout {
            Mycroft.AutoFitLabel {
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 3
                text: "Humidity:"
            }
            Mycroft.AutoFitLabel {
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 15
                text: sessionData.humidity + "%"
            }
        }
        ColumnLayout {
            Mycroft.AutoFitLabel {
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 3
                text: "Windspeed:"
            }
            Mycroft.AutoFitLabel {
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 15
                text: sessionData.wind
            }
        }
    }
}
