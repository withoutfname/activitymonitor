import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    minimumWidth: 1280
    minimumHeight: 720
    title: "Приложение"

    RowLayout {
        anchors.fill: parent

        ListView {
            id: navigation
            width: 200
            Layout.fillHeight: true

            model: ListModel {
                ListElement { name: "Главная"; file: "main.qml" }
                ListElement { name: "Конфигурация"; file: "config.qml" }
            }

            delegate: Item {
                width: parent.width
                height: 50  // Увеличим высоту для лучшего отображения

                Rectangle {
                    anchors.fill: parent
                    color: "transparent"  // Чтобы отступ был очевидным
                    implicitHeight: 40

                    Button {
                        anchors.fill: parent
                        anchors.margins: 10

                        text: model.name
                        onClicked: {
                            contentLoader.source = model.file
                        }
                    }
                }
            }
        }

        Loader {
            id: contentLoader
            Layout.fillWidth: true
            Layout.fillHeight: true
            anchors.margins: 10
            source: "main.qml"
        }
    }
}
