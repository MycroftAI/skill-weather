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
Re-usable code that defines a map of Open Weather Map icon codes to animations.

This code is specific to the Mark II device.  It uses images instead of animations to
address performance concerns.  Could change to use animations if the performance improves
*/
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.ProportionalDelegate {
    id: root
    skillBackgroundColorOverlay: Qt.rgba(0, 0, 0, 1)

    function getWeatherImagery(weathercode) {
        switch(weathercode) {
        case 0:
            return "animations/sunny.json";
            break
        case 1:
            return "animations/partlycloudy.json";
            break
        case 2:
            return "animations/cloudy.json";
            break
        case 3:
            return "animations/rain.json";
            break
        case 4:
            return "animations/rain.json";
            break
        case 5:
            return "animations/storm.json";
            break
        case 6:
            return "animations/snow.json";
            break
        case 7:
            return "animations/fog.json";
            break
        }
    }

}
