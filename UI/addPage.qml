import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.2

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightblue"

        ListView {
            id: listView
            anchors.fill: parent
            model: installedAppsDiff // Модель установленных приложений, переданная из Python

            delegate: Item {
                width: ListView.view.width
                height: 50

                RowLayout {
                    width: parent.width
                    height: parent.height

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
                            font.pixelSize: 18
                        }
                    }
                }
            }
        }

        Button {
            text: "Сохранить"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            onClicked: {
                if (selectedAppsToAdd.length === 0) {
                    messageDialog.open()
                } else {
                    appManager.saveAppsToDatabase(selectedAppsToAdd)
                    selectedAppsToAdd = []

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
