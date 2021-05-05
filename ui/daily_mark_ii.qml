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
Shows up to four days of forecasted weather.

Will be displayed when the user asks for a daily weather forecast.

This code is specific to the Mark II device.  It uses a grid of 32x32 pixel
squares for alignment of items.
*/
import QtQuick 2.4
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.4

WeatherDelegateMarkII {
    Item {
        // Bounding box for the content of the screen.
        id: dailyCard
        height: parent.height
        width: parent.width

        WeatherLocation {
            id: weatherLocation
        }

        RowLayout {
            // Four rows, one for each hour of the forecast.
            id: hourlyWeather
            anchors.left: parent.left
            anchors.leftMargin: gridUnit * 2
            anchors.top: weatherLocation.bottom
            anchors.topMargin: gridUnit * 2
            spacing: gridUnit * 2

            DailyColumn {
                forecast: sessionData.dailyForecast.days[0]
            }

            DailyColumn {
                forecast: sessionData.dailyForecast.days[1]
            }

            DailyColumn {
                forecast: sessionData.dailyForecast.days[2]
            }

            DailyColumn {
                forecast: sessionData.dailyForecast.days[3]
            }
        }
    }
}
