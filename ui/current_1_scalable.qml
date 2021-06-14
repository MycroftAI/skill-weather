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

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherDelegateScalable {
    id: root

    spacing: proportionalGridUnit * 5

    LottieAnimation {
        // Animation depicting the current weather conditions (e.g. sunny, cloudy, etc.)
        id: weatherAnimation
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: Math.min(root.contentWidth, proportionalGridUnit * 50)
        Layout.preferredHeight: Layout.preferredWidth

        source: Qt.resolvedUrl(getWeatherImagery(sessionData.weatherCode))

        loops: Animation.Infinite
        fillMode: Image.PreserveAspectFit
        running: true

        // Debug:
        onSourceChanged: {
            console.log(getWeatherImagery(sessionData.weatherCode));
        }
        onStatusChanged: {
            console.log(weatherAnimation.status, errorString);
        }
    }

    Label {
        //  Current temperature in the configured temperature unit
        id: temperature
        font.weight: Font.Bold
        font.pixelSize: parent.height * 0.65
        horizontalAlignment: Text.AlignHCenter
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        rightPadding: -font.pixelSize * 0.1
        text: sessionData.currentTemperature + "°"
    }
}
