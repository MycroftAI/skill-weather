import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

ForecastDelegate {
    id: root
    model: sessionData.forecast.second
}
