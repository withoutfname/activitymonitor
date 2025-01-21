import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightcoral"

        Text {
            anchors.centerIn: parent
            text: "Это страница кастомных"
            font.pixelSize: 24
        }
    }
}