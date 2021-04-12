import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherMarkIIDelegate {
    id: root

    Item {
        // Bounding box for the content of the screen.
        id: card
        height: parent.height
        width: parent.width

        GridLayout {
            id: weather
            anchors.left: parent.left
            anchors.leftMargin: 32
            anchors.top: parent.top
            anchors.topMargin: 32
            columns: 2
            columnSpacing: 32
            rowSpacing: 0

            Column {
                id: wind
                height: 352
                width: 320

                Item {
                    id: windIconBox
                    height: 128
                    width: parent.width

                    Image {
                        id: windIcon
                        anchors.top: parent.top
                        anchors.horizontalCenter: parent.horizontalCenter
                        fillMode: Image.PreserveAspectFit
                        height: parent.height
                        source: Qt.resolvedUrl("images/wind.svg")
                    }
                }

                Item {
                    id: windSpeedBox
                    anchors.top: windIconBox.bottom
                    anchors.topMargin: 32
                    height: 160
                    width: parent.width

                    Label {
                        id: windSpeed
                        anchors.baseline: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: "Noto Sans Display"
                        font.weight: Font.Bold
                        font.pixelSize: 176
                        text: sessionData.windSpeed
                    }
                }
            }

            Column {
                id: humidity
                height: 352
                width: 320

                Item {
                    id: humidityIconBox
                    height: 128
                    width: parent.width

                    Image {
                        id: humidityIcon
                        anchors.top: parent.top
                        anchors.horizontalCenter: parent.horizontalCenter
                        fillMode: Image.PreserveAspectFit
                        height: parent.height
                        source: Qt.resolvedUrl("images/humidity.svg")
                    }
                }

                Item {
                    id: humidityValueBox
                    anchors.top: humidityIconBox.bottom
                    anchors.topMargin: 32
                    height: 160
                    width: parent.width

                    Label {
                        id: humidityValue
                        anchors.baseline: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: "Noto Sans Display"
                        font.pixelSize: 180
                        font.weight: Font.Bold
                        text: sessionData.humidity
                    }
                }
            }
        }
    }
}
