// Copyright 2021, Mycroft AI Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.import QtQuick.Layouts 1.4

/*
One of many screns that show when the user asks for the current weather.

Shows an image representing current conditions and the current temperature.

This code written to be scalable for different screen sizes.  It can be used on any
device not conforming to the Mark II screen's form factor.
*/
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami
import QtQuick.Layouts 1.4
import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherDelegateScalable {
    id: root

    Rectangle {
        width: parent.width
        height: parent.height
        color: "black"

        WeatherLocation {
            id: weatherLocation
            fontSize: parent.height > parent.width ? parent.width * 0.10 : 45
        }

        GridLayout {
            id: weather
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.top: weatherLocation.bottom
            anchors.topMargin: Mycroft.Units.gridUnit * 2
            columns: 2
            columnSpacing: Mycroft.Units.gridUnit * 2

            Item {
                //First column in grid
                id: currentConditions
                Layout.fillWidth: true
                Layout.fillHeight: true

                Item {
                    width: parent.width
                    height: parent.height / 2

                    Image {
                        //Image depicting the current weather conditions (e.g. sunny, cloudy, etc.)
                        id: weatherAnimation
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: Mycroft.Units.gridUnit
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: parent.width - Mycroft.Units.gridUnit * 2
                        height: parent.height > parent.width ? width : parent.height - Mycroft.Units.gridUnit * 2
                        source: Qt.resolvedUrl(getWeatherImagery(sessionData.weatherCode))
                        fillMode: Image.PreserveAspectFit
                    }
                }

                Label {
                    //Current temperature in the configured temperature unit
                    id: temperature
                    font.weight: Font.Bold
                    font.pixelSize: parent.height > parent.width ? parent.width * 0.65 : parent.height * 0.65
                    anchors.baseline: parent.bottom
                    anchors.baselineOffset: -Mycroft.Units.gridUnit
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    rightPadding: -font.pixelSize * 0.1
                    font.family: "Noto Sans"
                    font.styleName: "Bold"
                    text: sessionData.currentTemperature + "°"
                }
            }

            ColumnLayout {
                //Second column in grid
                id: highLowTemperature
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: Mycroft.Units.gridUnit * 2

                Item {
                    //High temperature for today
                    id: highTemperature
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Item {
                        anchors.left: parent.left
                        width: parent.width * 0.40
                        height: parent.height

                        Kirigami.Icon {
                            id: highTemperatureIcon
                            anchors.right: parent.right
                            anchors.rightMargin: Mycroft.Units.gridUnit
                            height: parent.height > parent.width ? parent.width * 0.40 : parent.height * 0.40
                            width: height
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: Mycroft.Units.gridUnit
                            source: Qt.resolvedUrl("images/high_temperature.svg")
                        }
                    }

                    Item {
                        anchors.right: parent.right
                        width: parent.width * 0.60
                        height: parent.height

                        Label {
                            id: highTemperatureValue
                            width: parent.width
                            height: parent.height
                            anchors.baseline: parent.bottom
                            anchors.baselineOffset: -Mycroft.Units.gridUnit
                            font.family: "Noto Sans"
                            font.pixelSize: parent.height > parent.width ? parent.width * 0.65 : parent.height * 0.85
                            font.styleName: "SemiBold"
                            text: sessionData.highTemperature + "°"
                        }
                    }
                }

                Item {
                    //Low temperature for today
                    id: lowTemperature
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Item {
                        anchors.left: parent.left
                        width: parent.width * 0.40
                        height: parent.height

                        Kirigami.Icon {
                            id: lowTemperatureIcon
                            anchors.right: parent.right
                            anchors.rightMargin: Mycroft.Units.gridUnit
                            height: parent.height > parent.width ? parent.width * 0.40 : parent.height * 0.40
                            width: height
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: Mycroft.Units.gridUnit
                            source: Qt.resolvedUrl("images/low_temperature.svg")
                        }
                    }

                    Item {
                        anchors.right: parent.right
                        width: parent.width * 0.60
                        height: parent.height

                        Label {
                            id: lowTemperatureValue
                            width: parent.width
                            height: parent.height
                            anchors.baseline: parent.bottom
                            anchors.baselineOffset: -Mycroft.Units.gridUnit
                            font.family: "Noto Sans"
                            font.pixelSize: parent.height > parent.width ? parent.width * 0.65 : parent.height * 0.85
                            font.styleName: "Light"
                            text: sessionData.lowTemperature + "°"
                        }
                    }
                }
            }
        }
    }
}
