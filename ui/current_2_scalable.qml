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
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherScalableDelegate {
    id: root

    Mycroft.AutoFitLabel {
        id: highTemperature
        font.weight: Font.Bold
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        //The off-centering to balance the ° should be proportional as well, so we use the computed pixel size
        rightPadding: -font.pixelSize * 0.1
        text: sessionData.highTemperature + "°"
    }

    Mycroft.AutoFitLabel {
        id: lowTemperature
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        rightPadding: -font.pixelSize * 0.1
        font.weight: Font.Thin
        font.styleName: "Thin"
        text: sessionData.lowTemperature + "°"
    }
}
