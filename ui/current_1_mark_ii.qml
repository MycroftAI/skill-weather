/*
One of many screns that show when the user asks for the current weather.

Shows an animation with current conditions, the current temperature, and
the high/low temperature for today.

This code is specific to the Mark II device.  It uses a grid of 32x32 pixel
squares for alignment of items.
*/
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft
import org.kde.lottie 1.0

WeatherMarkIIDelegate {
    id: root

    Item {
        // Bounding box for the content of the screen.
        id: card
        height: parent.height
        width: parent.width

        Item {
            // City/state if in same country as device.  City/country if in a different country
            id: weatherLocation
            height: 64
            width: parent.width

            Label {
                id: weatherLocationText
                anchors.baseline: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: "Noto Sans Display"
                font.pixelSize: 48
                text: "Kansas City, Missouri"
            }
        }

        GridLayout {
            id: weather
            anchors.left: parent.left
            anchors.leftMargin: 32
            anchors.top: weatherLocation.bottom
            anchors.topMargin: 32
            columns: 2
            columnSpacing: 32

            Item {
                // First row in grid
                id: currentConditions
                height: 288
                width: 320

                Image {
                    // Image depicting the current weather conditions (e.g. sunny, cloudy, etc.)
                    id: conditionsImage
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.horizontalCenterOffset: -32
                    fillMode: Image.PreserveAspectFit
                    height: 112
                    source: Qt.resolvedUrl(getWeatherImagery(sessionData.weatherCode))
                }

                Label {
                    //  Current temperature in the configured temperature unit.
                    id: currentTemperature
                    anchors.baseline: parent.bottom
                    anchors.baselineOffset: -16
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.family: "Noto Sans Display"
                    font.pixelSize: 176
                    font.weight: Font.Bold
                    text: sessionData.currentTemperature + "°"
                }
            }

            Column {
                // Second column
                id: highLowTemperature
                height: 288
                width: 320
                spacing: 32

                Item {
                    // High temperature for today
                    id: highTemperature
                    height: 128
                    width: parent.width

                    Image {
                        id: highTemperatureIcon
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 32
                        anchors.left: highTemperature.left
                        anchors.leftMargin: 32
                        fillMode: Image.PreserveAspectFit
                        height: 64
                        source: Qt.resolvedUrl("images/high_temperature.svg")
                    }

                    Label {
                        id: highTemperatureValue
                        anchors.baseline: parent.bottom
                        anchors.baselineOffset: -32
                        anchors.left: highTemperatureIcon.right
                        anchors.leftMargin: 32
                        font.family: "Noto Sans Display"
                        font.pixelSize: 118
                        font.weight: Font.Bold
                        text: sessionData.highTemperature + "°"
                    }
                }

                Item {
                    // Low temperature for today
                    id: lowTemperature
                    height: 128
                    width: parent.width

                    Image {
                        id: lowTemperatureIcon
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 32
                        anchors.left: lowTemperature.left
                        anchors.leftMargin: 32
                        fillMode: Image.PreserveAspectFit
                        height: 64
                        source: Qt.resolvedUrl("images/low_temperature.svg")
                    }

                    Label {
                        id: lowTemperatureValue
                        anchors.baseline: parent.bottom
                        anchors.baselineOffset: -32
                        anchors.left: lowTemperatureIcon.right
                        anchors.leftMargin: 32
                        font.family: "Noto Sans Display"
                        font.pixelSize: 118
                        font.weight: Font.Light
                        text: sessionData.lowTemperature + "°"
                    }
                }
            }
        }
    }
}
