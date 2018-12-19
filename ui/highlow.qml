import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

Mycroft.Delegate {
    skillBackgroundSource: Qt.resolvedUrl("img/bg.png")

    ColumnLayout {
        id: grid
        Layout.fillWidth: true
        anchors.centerIn: parent
        spacing: 0

        Label {
            id: maxTemp
            Layout.alignment: Qt.AlignHCenter
            font.capitalization: Font.AllUppercase
            font.family: "Noto Sans Display"
            font.weight: Font.Bold
            font.pixelSize: 240
            color: "white"
            lineHeight: 0.6
            text: sessionData.max + "°"
        }
        Item {
            height: Kirigami.Units.largeSpacing * 10
        }
        Label {
            id: minTemp
            Layout.alignment: Qt.AlignHCenter
            font.capitalization: Font.AllUppercase
            font.family: "Noto Sans Display"
            font.pixelSize: 240
            font.styleName: "Thin"
            color: "white"
            lineHeight: 0.6
            text: sessionData.min + "°"
        }
    }
}
