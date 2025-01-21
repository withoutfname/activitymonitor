import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightgreen"

        ColumnLayout {
            anchors.fill: parent
            spacing: 10
            anchors.margins: 10

            // Кнопка "Старт" или "Стоп"
            RowLayout {
                Layout.alignment: Qt.AlignTop | Qt.AlignLeft // Привязываем к верхнему левому углу
                spacing: 10

                Button {
                    id: startButton
                    text: "Начать отслеживание"
                    visible: appManager ? !appManager.isTracking : false
                    onClicked: {
                        if (appManager) {
                            appManager.startTracking();
                        }
                    }
                }

                Button {
                    id: stopButton
                    text: "Остановить отслеживание"
                    visible: appManager ? appManager.isTracking : false
                    onClicked: {
                        if (appManager) {
                            appManager.stopTracking();
                        }
                    }
                }
            }

            // Поле поиска и кнопка "Обновить"
            RowLayout {
                visible: appManager ? appManager.isTracking : false
                Layout.fillWidth: true
                spacing: 10

                TextField {
                    id: searchField
                    width: 600
                    placeholderText: "Поиск по названию"
                    onTextChanged: {
                        if (openedWindowsModel) {
                            openedWindowsModel.filter(text);
                        }
                    }
                }

                Button {
                    text: "Обновить"
                    onClicked: {
                        if (appManager) {
                            appManager.updateOpenedWindows();
                        }
                    }
                }

                Button {
                    text: "Сохранить"
                    onClicked: {
                        if (appManager && selectedAppsToAdd.length === 0) {
                            messageDialog.open()
                        } else if (appManager) {
                            appManager.saveAppsToDatabase(selectedAppsToAdd)
                            selectedAppsToAdd = [] // Очистка массива после сохранения
                        }
                    }
                }
            }

            // Список открытых окон
            ListView {
                id: listView
                width: 700
                Layout.fillHeight: true
                model: openedWindowsModel
                spacing: 5
                visible: appManager ? appManager.isTracking : false

                delegate: Rectangle {
                    width: listView.width
                    height: 80
                    color: "white"
                    border.color: "lightgray"
                    radius: 5

                    RowLayout {
                        anchors.fill: parent
                        spacing: 10
                        anchors.margins: 10

                        // Чекбокс для выбора приложения
                        CheckBox {
                            id: checkBox
                            Layout.alignment: Qt.AlignVCenter
                        }

                        // Информация о приложении
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 5

                            Text {
                                text: model.title
                                font.pixelSize: 16
                                font.bold: true
                                elide: Text.ElideRight
                                horizontalAlignment: Text.AlignHCenter
                                Layout.fillWidth: true
                            }

                            Text {
                                text: "Процесс: " + model.processName
                                font.pixelSize: 14
                                elide: Text.ElideRight
                                horizontalAlignment: Text.AlignHCenter
                                Layout.fillWidth: true
                            }

                            Text {
                                text: "Путь: " + model.exePath
                                font.pixelSize: 14
                                elide: Text.ElideRight
                                horizontalAlignment: Text.AlignHCenter
                                Layout.fillWidth: true
                            }
                        }
                    }
                }
            }
        }
    }
}