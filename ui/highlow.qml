import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherDelegate {
    id: root

    Mycroft.AutoFitLabel {
        id: maxTemp
        font.weight: Font.Bold
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        //The off-centering to balance the ° should be proportional as well, so we use the computed pixel size
        rightPadding: -font.pixelSize * 0.1
        text: sessionData.max + "°"
    }

    Mycroft.AutoFitLabel {
        id: minTemp
        Layout.fillWidth: true
        Layout.preferredHeight: proportionalGridUnit * 40
        rightPadding: -font.pixelSize * 0.1
        font.weight: Font.Thin
        font.styleName: "Thin"
        text: sessionData.min + "°"
    }
}
