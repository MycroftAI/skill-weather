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
Abstract component for alphanunumeric values.

The Mark II card design requires the ability to have a text field's baseline sit on one
of the 16 pixel grid lines.  The benefit of this approach is consistent alignment of
text fields that disregards the extra space that can be included around the text for
ascenders and descenders.

To implement this idea, a bounding box is defined around a label for alignment purposes.
The baseline of the text sits on the bottom of the bounding box and the value is
centered within the box.

This code is specific to the Mark II device.  It uses a grid of 16x16 pixel
squares for alignment of items.
*/
import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.3

Item {
    property alias fontSize: weatherLabel.font.pixelSize
    property alias fontStyle: weatherLabel.font.styleName
    property alias text: weatherLabel.text
    property int heightUnits

    height: gridUnit * heightUnits
    width: parent.width

    Label {
        id: weatherLabel
        anchors.baseline: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: "Noto Sans Display"
    }
}
