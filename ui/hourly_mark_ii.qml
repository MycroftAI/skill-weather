//import QtQuick.Layouts 1.4
//import QtQuick 2.4
//import QtQuick.Controls 2.0
//import org.kde.kirigami 2.4 as Kirigami
//
//import Mycroft 1.0 as Mycroft
//import org.kde.lottie 1.0
//
//ForecastMarkIIDelegate {
//    id: root
//    model: sessionData.forecast.first
//}
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherMarkIIDelegate {
    Item {
        id: hourlyCard
        height: parent.height
        width: parent.width

        GridLayout {
            id: currentWeather
            anchors.left: parent.left
            anchors.leftMargin: 32
            anchors.top: parent.top
            anchors.topMargin: 32
            columns: 4
            columnSpacing: 32
            rowSpacing: 0
            Layout.fillWidth: true

            Repeater {
                id: conditionRepeater
                model: sessionData.weatherCodes
                anchors.top: parent.top

                Item {
                    height: 64
                    width: 144

                    Image {
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.top: parent.top
                        height: 64
                        fillMode: Image.PreserveAspectFit
                        source: Qt.resolvedUrl(getWeatherImagery(modelData))
                    }
                }
            }

            Repeater {
                id: timeRepeater
                model: sessionData.times

                Item {
                    height: 64
                    width: 144

                    Label {
                        anchors.baseline: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: "Noto Sans Display"
                        font.pixelSize: 59
                        text: modelData
                    }
                }
            }

            Repeater {
                id: temperatureRepeater
                model: sessionData.temperatures

                Item {
                    height: 96
                    width: 144

                    Label {
                        anchors.baseline: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: "Noto Sans Display"
                        font.pixelSize: 72
                        font.weight: Font.Bold
                        text: modelData + "°"
                    }
                }
            }

            Repeater {
                id: precipitationRepeater
                model: sessionData.chancesOfPrecipitation

                Item {
                    height: 96
                    width: 144

                    Label {
                        anchors.baseline: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.family: "Noto Sans Display"
                        font.pixelSize: 59
                        font.weight: Font.Thin
                        text: modelData + "%"
                    }
                }
            }
        }
    }
}
