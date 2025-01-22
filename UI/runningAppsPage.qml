import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    property var runningAppsToAdd: []

    Rectangle {
        anchors.fill: parent
        color: "lightgreen"

        ColumnLayout {
            anchors.fill: parent
            spacing: 10
            anchors.margins: 10

            // Поле поиска и кнопка "Обновить"
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Layout.bottomMargin: 50

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
                        runningAppsToAdd = [];
                        openedWindowsManager.updateOpenedWindows(); // Используем openedWindowsManager
                    }
                }

                Button {
                    text: "Сохранить"
                    onClicked: {
                        if (runningAppsToAdd.length === 0) {
                            messageDialog.open();
                        } else {
                            databaseManager.saveAppsToDatabase(runningAppsToAdd); // Сохраняем в БД
                            runningAppsToAdd = []; // Очищаем массив
                            trackedAppsManager.updateTrackedApps(); // Обновляем список отслеживаемых приложений
                            openedWindowsManager.updateOpenedWindows(); // Обновляем список открытых окон

                        }
                    }
                }
            }

            // Список открытых окон
            ListView {
                id: listView
                width: 700
                Layout.fillHeight: true
                Layout.topMargin: 20
                Layout.bottomMargin: 20
                model: openedWindowsModel
                spacing: 5

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

                            // Устанавливаем начальное состояние чекбокса
                            Component.onCompleted: {
                                checkBox.checked = runningAppsToAdd.some(app => app.processName === model.processName);
                            }

                            onCheckedChanged: {
                                if (checked) {
                                    // Добавляем приложение в массив, если чекбокс отмечен
                                    runningAppsToAdd.push({
                                        title: model.title,
                                        processName: model.processName,
                                        exePath: model.exePath
                                    });
                                } else {
                                    // Удаляем приложение из массива, если чекбокс снят
                                    runningAppsToAdd = runningAppsToAdd.filter(app => app.processName !== model.processName);
                                }
                            }
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

    // Диалог для отображения ошибок
    Dialog {
        id: messageDialog
        title: "Ошибка"
        standardButtons: Dialog.Ok
        width: 300
        height: 200
        contentItem: Text {
            text: "Выберите хотя бы одно приложение"
            wrapMode: Text.WordWrap
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        onAccepted: {
            messageDialog.close();
        }
    }

    // Автоматическое обновление списка при загрузке страницы
    Component.onCompleted: {
        runningAppsToAdd = [];
        openedWindowsManager.updateOpenedWindows(); // Используем openedWindowsManager
    }
}