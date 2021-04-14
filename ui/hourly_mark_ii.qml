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
Shows up to four hours of forecasted weather.

Will be displayed when:
    * the user asks for a hourly weather forecast.
    * as the last screen when a user asks for current weather.

This code is specific to the Mark II device.  It uses a grid of 32x32 pixel
squares for alignment of items.
*/
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherMarkIIDelegate {
    Item {
        // Bounding box for the content of the screen.
        id: hourlyCard
        height: parent.height
        width: parent.width

        GridLayout {
            // Four column grid, one for each hour of the forecast.
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
                // Displays one to four hours of images representing weather conditions
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
                // Displays one to four hours of the time.
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
                // Displays one to four hours of the forecasted temperature
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
                // Displays one to four hours of the forecasted chance of precipitation
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
