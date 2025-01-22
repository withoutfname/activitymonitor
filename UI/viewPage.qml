import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightblue"

        // Сообщение, если список пуст
        Label {
            id: emptyListMessage
            anchors.centerIn: parent
            text: "Нет отслеживаемых приложений"
            font.pixelSize: 20
            visible: trackedAppsModel.count === 0 // Показываем, если список пуст
        }

        // Список отслеживаемых приложений
        ListView {
            anchors.fill: parent
            model: trackedAppsModel // Используем trackedAppsModel
            visible: trackedAppsModel.count > 0 // Показываем, если есть приложения

            delegate: Item {
                width: ListView.view.width
                height: 50

                Rectangle {
                    width: parent.width
                    height: 50
                    color: "white"
                    border.color: "black"
                    radius: 5

                    Text {
                        anchors.centerIn: parent
                        text: name // Отображаем имя приложения
                        font.pixelSize: 18
                    }
                }
            }
        }
    }
}