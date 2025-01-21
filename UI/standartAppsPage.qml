import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    ColumnLayout {
        anchors.fill: parent
        spacing: 10
        anchors.margins: 10

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            TextField {
                width: 600
                placeholderText: "Введите поисковое значение"
                onTextChanged: {
                    // Фильтрация списка приложений по введенному тексту
                    listView.model = installedAppsDiff.filter(function(app) {
                        return app.name.toLowerCase().includes(text.toLowerCase());
                    });
                }
            }

            Button {
                text: "Обновить"
                onClicked: {
                    // Логика обновления списка приложений
                    appManager.updateInstalledAppsDiff()
                }
            }

            Button {
                text: "Сохранить"
                onClicked: {
                    if (selectedAppsToAdd.length === 0) {
                        messageDialog.open()
                    } else {
                        appManager.saveAppsToDatabase(selectedAppsToAdd)
                        selectedAppsToAdd = [] // Очистка массива после сохранения
                    }
                }
            }
        }

        ListView {
            id: listView

            width: 700
            Layout.fillHeight: true
            model: notTrackedAppsModel // Используем модель из Python

            delegate: Item {
                width: 600
                height: 40

                RowLayout {
                    width: parent.width
                    height: parent.height
                    spacing: 10

                    CheckBox {
                        id: checkBox
                        Layout.alignment: Qt.AlignLeft
                        onCheckedChanged: {
                            console.log("Selected:", model.name)
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "white"
                        border.color: "black"
                        radius: 5

                        Text {
                            anchors.centerIn: parent
                            text: model.name
                            font.pixelSize: 14
                            elide: Text.ElideRight
                        }
                    }
                }
            }
        }
    }

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
            messageDialog.close()
        }
    }
}