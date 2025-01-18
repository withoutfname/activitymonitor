import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightblue"

        ListView {
            anchors.fill: parent
            model: installedAppsDB // Модель установленных приложений, переданная из Python

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
                        text: modelData.name
                        font.pixelSize: 18
                    }
                }
            }
        }
    }
}
