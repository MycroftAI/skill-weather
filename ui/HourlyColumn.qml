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

This code is specific to the Mark II device.  It uses a grid of 16x16 pixel
squares for alignment of items.
*/
import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.3

Column {
    id: hourlyColumn
    spacing: gridUnit * 2
    width: gridUnit * 9

    property var forecast

    WeatherImage {
        id: forecastCondition
        heightUnits: 4
        imageSource: forecast.weatherCondition
    }

    WeatherLabel {
        id: forecastTime
        heightUnits: 2
        fontSize: 47
        fontStyle: "Regular"
        text: forecast.time
    }

    WeatherLabel {
        id: forecastTemperature
        heightUnits: 3
        fontSize: 72
        fontStyle: "Bold"
        text: forecast.temperature + "°"
    }

    WeatherLabel {
        id: forecastPrecipitation
        heightUnits: 3
        fontSize: 72
        fontStyle: "Light"
        text: forecast.precipitation + "%"
    }
}

