import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

Mycroft.Delegate {
    id: top
    skillBackgroundSource: Qt.resolvedUrl("img/bg.png")
    function getWeatherImagery(weathercode){
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

    ColumnLayout {
        id: grid
        anchors.centerIn: parent
        spacing: 0
        Rectangle {
        Label {
            id: location
            font.family: "Noto Sans Display"
            font.weight: Font.Bold
            font.pixelSize: 30
            color: "white"
            wrapMode: Text.WordWrap
            text: sessionData.location
            lineHeight: 0.6
        }}
        Item {
            height: Kirigami.Units.largeSpacing * 10
        }
        LottieAnimation {
            id: weatherAnimation
            Layout.preferredWidth: Kirigami.Units.gridUnit * 14
            Layout.preferredHeight: Kirigami.Units.gridUnit * 14
            source: Qt.resolvedUrl(getWeatherImagery(sessionData.weathercode))
            //source: Qt.resolvedUrl("animations/sunny.json")
            loops: Animation.Infinite
            fillMode: Image.PreserveAspectFit
            running: true

            // Debug:
            onSourceChanged: {
                console.log(getWeatherImagery(sessionData.weathercode));
            }
            onStatusChanged: {
                console.log(fancyAnimation.status, errorString);
            }
        }
        Item {
            height: Kirigami.Units.largeSpacing * 5
        }
        
        GridLayout {
            columns: 2
            columnSpacing: Kirigami.Units.largeSpacing * 3
            rowSpacing: Kirigami.Units.largeSpacing * 3
            ColumnLayout {
                Label {
                    id: min_lable
                    Layout.alignment: Qt.AlignHRight
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 15
                    color: "white"
                    lineHeight: 0.6
                    text: "Min:"
                }
                Label {
                    id: min
                    Layout.alignment: Qt.AlignHCenter
                    font.capitalization: Font.AllUppercase
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 120
                    color: "white"
                    lineHeight: 0.6
                    text: sessionData.min + "°"
                }
            }
            ColumnLayout {
                Label {
                    id: max_lable
                    Layout.alignment: Qt.AlignHRight
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 15
                    color: "white"
                    lineHeight: 0.6
                    text: "Max:"
                }
                Label {
                    id: max
                    Layout.alignment: Qt.AlignHCenter
                    font.capitalization: Font.AllUppercase
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 120
                    color: "white"
                    lineHeight: 0.6
                    text: sessionData.max + "°"
                }
            }
            ColumnLayout {
                Label {
                    id: humidity_label
                    Layout.alignment: Qt.AlignHRight
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 15
                    color: "white"
                    lineHeight: 0.6
                    text: "Humidity:"
                }
                Label {
                    id: humidity
                    Layout.alignment: Qt.AlignHCenter
                    font.capitalization: Font.AllUppercase
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 120
                    color: "white"
                    lineHeight: 0.6
                    text: sessionData.humidity + "﹪" // Small percent
                }
            }
            ColumnLayout {
                Label {
                    id: wind_label
                    Layout.alignment: Qt.AlignHRight
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 15
                    color: "white"
                    lineHeight: 0.6
                    text: "Windspeed:"
                }
                Label {
                    id: wind
                    Layout.alignment: Qt.AlignHCenter
                    font.capitalization: Font.AllUppercase
                    font.family: "Noto Sans Display"
                    font.weight: Font.Bold
                    font.pixelSize: 120
                    color: "white"
                    lineHeight: 0.6
                    text: sessionData.wind
                }
            }
        }
    }
}
