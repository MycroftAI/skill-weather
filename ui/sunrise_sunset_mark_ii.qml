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
Screen for showing the sunrise and snset.

This code is specific to the Mark II device.  It uses a grid of 16x16 pixel
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
            id: sunriseSunset
            anchors.left: parent.left
            anchors.leftMargin: gridUnit * 2
            anchors.top: weatherLocation.bottom
            anchors.topMargin: gridUnit * 2
            columns: 2
            columnSpacing: gridUnit * 2
            width: gridUnit * 20

            Column {
                // First column in grid
                id: sunrise
                height: gridUnit * 22
                spacing: gridUnit * 2
                width: parent.width

                WeatherImage {
                    id: sunriseImage
                    heightUnits: 5
                    imageSource: "images/sunrise.svg"
                }

                WeatherLabel {
                    id: sunriseTime
                    heightUnits: 4
                    fontSize: 82
                    fontStyle: "Bold"
                    text: sessionData.sunrise
                }

                WeatherLabel {
                    id: sunriseAm
                    heightUnits: 2
                    fontSize: 60
                    fontStyle: "Regular"
                    text: sessionData.ampm ? "AM" : ""
                }
            }

            Column {
                // Second column in grid
                id: sunset
                height: gridUnit * 22
                spacing: gridUnit * 2
                width: parent.width

                WeatherImage {
                    id: sunsetImage
                    heightUnits: 5
                    imageSource: "images/sunset.svg"
                }

                WeatherLabel {
                    id: sunsetTime
                    heightUnits: 4
                    fontSize: 82
                    fontStyle: "Bold"
                    text: sessionData.sunset
                }

                WeatherLabel {
                    id: sunsetPm
                    heightUnits: 2
                    fontSize: 60
                    fontStyle: "Regular"
                    text: sessionData.ampm ? "PM" : ""
                }
            }
        }
    }
}
