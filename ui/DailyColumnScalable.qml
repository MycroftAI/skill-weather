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
Define the default values for a weather forecast column.

A forecast screen has four columns, each with the same data.  This abstracts out the
common bits of each column.
*/
import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.3
import org.kde.kirigami 2.4 as Kirigami
import Mycroft 1.0 as Mycroft

Column {
    id: dailyColumn
    property var forecast

    onForecastChanged: {
        console.log(JSON.stringify(forecast))
    }

    Item {
        height: parent.height * 0.25
        anchors.left: parent.left
        anchors.right: parent.right

        Image {
            anchors.fill: parent
            source: Qt.resolvedUrl(forecast.weatherCondition)
            fillMode: Image.PreserveAspectFit
        }
    }

    Label {
        anchors.left: parent.left
        anchors.right: parent.right

        height: parent.height * 0.25
        horizontalAlignment: Text.AlignHCenter
        font.weight: Font.Bold
        font.pixelSize: width * 0.2
        color: "white"
        text: forecast.date
    }

    Label {
        anchors.left: parent.left
        anchors.right: parent.right
        horizontalAlignment: Text.AlignHCenter

        font.weight: Font.Bold
        font.pixelSize: width * 0.2
        height: parent.height * 0.25
        color: "white"
        text: forecast.highTemperature + "°"
    }

    Label {
        anchors.left: parent.left
        anchors.right: parent.right
        horizontalAlignment: Text.AlignHCenter

        font.styleName: "Thin"
        font.pixelSize: width * 0.2
        height: parent.height * 0.25
        color: "white"
        text: forecast.lowTemperature + "°"
    }
}

