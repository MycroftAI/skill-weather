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
// limitations under the License.

/*
One of many screns that show when the user asks for the current weather.

Shows an image representing current conditions, the current temperature, and
the high/low temperature for today.

This code is specific to the Mark II device.  It uses a grid of 32x32 pixel
squares for alignment of items.
*/
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0

WeatherDelegateMarkII {
    id: root

    Item {
        // Bounding box for the content of the screen.
        id: card
        height: parent.height
        width: parent.width

        WeatherDate {
            id: weatherDate
        }

        WeatherLocation {
            id: weatherLocation
            anchors.top: weatherDate.bottom
        }

        GridLayout {
            id: weather
            anchors.left: parent.left
            anchors.leftMargin: gridUnit * 2
            anchors.top: weatherLocation.bottom
            anchors.topMargin: gridUnit * 2
            columns: 2
            columnSpacing: gridUnit * 2
            width: gridUnit * 20

            Item {
                // First column in grid
                id: weatherConditions
                height: gridUnit * 14
                width: parent.width

                WeatherImage {
                    id: forecastCondition
                    heightUnits: 6
                    imageSource: sessionData.weatherCondition
                }

                WeatherLabel {
                    id: precipitation
                    anchors.top: forecastCondition.bottom
                    anchors.topMargin: gridUnit * 2
                    heightUnits: 6
                    fontSize: 118
                    fontStyle: "Regular"
                    text: sessionData.chanceOfPrecipitation + "%"
                }

                Label {
                    //  Chance of precipitation for the day.
                    id: currentTemperature
                    anchors.baseline: parent.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.family: "Noto Sans Display"
                    font.pixelSize: 118
                    font.styleName: "Light"
                    text: sessionData.chanceOfPrecipitation + "%"
                }
            }

            Column {
                // Second column in grid
                id: highLowTemperature
                height: gridUnit * 14
                spacing: gridUnit * 2
                width: parent.width

                Item {
                    // High temperature for today
                    id: highTemperature
                    height: gridUnit * 6
                    width: parent.width

                    Image {
                        id: highTemperatureIcon
                        anchors.bottom: parent.bottom
                        anchors.left: highTemperature.left
                        anchors.leftMargin: gridUnit * 2
                        fillMode: Image.PreserveAspectFit
                        height: gridUnit * 4
                        source: Qt.resolvedUrl("images/high_temperature.svg")
                    }

                    Label {
                        id: highTemperatureValue
                        anchors.baseline: parent.bottom
                        anchors.left: highTemperatureIcon.right
                        anchors.leftMargin: gridUnit * 2
                        font.family: "Noto Sans Display"
                        font.pixelSize: 118
                        font.styleName: "SemiBold"
                        text: sessionData.highTemperature + "°"
                    }
                }

                Item {
                    // Low temperature for today
                    id: lowTemperature
                    height: gridUnit * 6
                    width: parent.width

                    Image {
                        id: lowTemperatureIcon
                        anchors.bottom: parent.bottom
                        anchors.left: lowTemperature.left
                        anchors.leftMargin: gridUnit * 2
                        fillMode: Image.PreserveAspectFit
                        height: gridUnit * 4
                        source: Qt.resolvedUrl("images/low_temperature.svg")
                    }

                    Label {
                        id: lowTemperatureValue
                        anchors.baseline: parent.bottom
                        anchors.left: lowTemperatureIcon.right
                        anchors.leftMargin: gridUnit * 2
                        font.family: "Noto Sans Display"
                        font.pixelSize: 118
                        font.styleName: "Light"
                        text: sessionData.lowTemperature + "°"
                    }
                }
            }
        }
    }
}
