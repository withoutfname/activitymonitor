import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 500
    height: 400
    title: "Installed Applications"

    ListView {
        anchors.fill: parent
        model: ListModel {
            ListElement { name: "Example App 1"; exePath: "C:/path/to/exe1" }
            ListElement { name: "Example App 2"; exePath: "C:/path/to/exe2" }
            ListElement { name: "Example App 3"; exePath: "C:/path/to/exe3" }
        }

        delegate: Item {
            width: parent.width
            height: 50

            Rectangle {
                width: parent.width
                height: 50
                color: "lightgray"
                border.color: "gray"

                Text {
                    anchors.centerIn: parent
                    text: name + " - " + exePath
                    font.pixelSize: 14
                }
            }
        }
    }
}
