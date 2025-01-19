import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.2

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightblue"

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
                Layout.alignment: Qt.AlignHCenter
                width: 700
                Layout.fillHeight: true
                model: installedAppsDiff // Модель установленных приложений, переданная из Python

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
                            checked: selectedAppsToAdd.indexOf(modelData.name) !== -1
                            onCheckedChanged: {
                                if (checkBox.checked) {
                                    if (selectedAppsToAdd.indexOf(modelData.name) === -1) {
                                        selectedAppsToAdd.push(modelData.name)
                                        console.log("Added to Add:", modelData.name)
                                    }
                                } else {
                                    var index = selectedAppsToAdd.indexOf(modelData.name)
                                    if (index > -1) {
                                        selectedAppsToAdd.splice(index, 1)
                                        console.log("Removed from Add:", modelData.name)
                                    }
                                }
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
                                text: modelData.name
                                font.pixelSize: 14
                                elide: Text.ElideRight
                            }
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
        contentItem: Text {
            text: "Выберите хотя бы одно приложение"
            wrapMode: Text.WordWrap
        }

        onAccepted: {
            messageDialog.close()
        }
    }
}
