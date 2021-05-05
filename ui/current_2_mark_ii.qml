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

Shows the current wind speed and percentage humidity.

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

        WeatherLocation {
            id: weatherLocation
        }

        GridLayout {
            // Two column grid containg wind and humidity data
            id: weather
            anchors.left: parent.left
            anchors.leftMargin: gridUnit * 2
            anchors.top: weatherLocation.bottom
            anchors.topMargin: gridUnit * 2
            columns: 2
            columnSpacing: gridUnit * 2
            rowSpacing: 0

            Column {
                // First column of the grid, displaying a wind icon and speed.
                id: wind
                height: gridUnit * 22
                width: gridUnit * 20
                spacing: gridUnit * 2

                WeatherImage {
                    id: windIcon
                    heightUnits: 8
                    imageSource: "images/wind.svg"
                }

                WeatherLabel {
                    id: windSpeed
                    fontSize: 176
                    fontStyle: "Bold"
                    heightUnits: 8
                    text: sessionData.windSpeed
                }
            }

            Column {
                // Second column of the grid, displaying a humidity icon and speed.
                id: humidity
                height: gridUnit * 22
                width: gridUnit * 20
                spacing: gridUnit * 2

                WeatherImage {
                    id: humidityIcon
                    heightUnits: 8
                    imageSource: "images/humidity.svg"
                }

                WeatherLabel {
                    id: humidityPercentage
                    fontSize: 176
                    fontStyle: "Bold"
                    heightUnits: 8
                    text: sessionData.humidity
                }
            }
        }
    }
}
