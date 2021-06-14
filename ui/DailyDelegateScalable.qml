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

    property alias model: forecastRepeater.model

    spacing: proportionalGridUnit * 10
    Repeater {
        id: forecastRepeater
        delegate: GridLayout {
            columns: 2
            rowSpacing: proportionalGridUnit * 5
            columnSpacing: proportionalGridUnit * 5
            Layout.fillWidth: true
            Layout.fillHeight: true

            LottieAnimation {
                Layout.alignment: Qt.AlignCenter
                Layout.preferredHeight: proportionalGridUnit * 30
                Layout.preferredWidth: Layout.preferredHeight

                source: Qt.resolvedUrl(modelData.weatherCondition)
                loops: Animation.Infinite
                fillMode: Image.PreserveAspectFit
                running: true
            }
            Label {
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 30
                font.pixelSize: height * 0.90
                text: modelData.date
            }

            Label {
                font.weight: Font.Bold
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 30
                rightPadding: -font.pixelSize * 0.1
                font.pixelSize: height * 0.90
                horizontalAlignment: Text.AlignHCenter
                text: modelData.highTemperature + "°"
            }

            Label {
                font.styleName: "Thin"
                Layout.fillWidth: true
                Layout.preferredHeight: proportionalGridUnit * 30
                rightPadding: -font.pixelSize * 0.1
                font.pixelSize: height * 0.90
                horizontalAlignment: Text.AlignHCenter
               text: modelData.lowTemperature + "°"
            }
        }
    }
}
