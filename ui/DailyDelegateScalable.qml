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
Re-usable code to display two days forecast.

This code written to be scalable for different screen sizes.  It can be used on any
device not conforming to the Mark II screen's form factor.
*/
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherDelegateScalable {
    id: root

    property var model

    Rectangle {
        width: parent.width
        height: parent.height
        color: "black"

        WeatherLocation {
            id: weatherLocationPageThree
            fontSize: parent.height > parent.width ? parent.width * 0.10 : 45
        }

        Item {
            anchors.top: weatherLocationPageThree.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.topMargin: Mycroft.Units.gridUnit * 2

            DailyColumnScalable {
                id: d1
                width: parent.width / 4
                height: parent.height
                anchors.left: parent.left
                forecast: model[0]
            }

            DailyColumnScalable {
                id: d2
                width: parent.width / 4
                height: parent.height
                anchors.left: d1.right
                forecast: model[1]
            }

            DailyColumnScalable {
                id: d3
                width: parent.width / 4
                height: parent.height
                anchors.right: d4.left
                forecast: model[2]
            }

            DailyColumnScalable {
                id: d4
                width: parent.width / 4
                height: parent.height
                anchors.right: parent.right
                forecast: model[3]
            }
        }
    }
}
