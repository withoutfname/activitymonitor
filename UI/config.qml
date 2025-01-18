import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    property var selectedAppsToAdd: []
    property var selectedAppsToRemove: []

    Rectangle {
        anchors.fill: parent
        color: "lightgreen"

        ColumnLayout {
            anchors.fill: parent
            spacing: 20

            // Кнопки навигации
            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                spacing: 10
                Layout.preferredHeight: 50 // Фиксированная высота для кнопок навигации

                Button {
                    text: "Просмотр"
                    onClicked: {
                        contentLoader.source = "viewPage.qml"
                    }
                }

                Button {
                    text: "Добавить"
                    onClicked: {
                        contentLoader.source = "addPage.qml"
                    }
                }

                Button {
                    text: "Удалить"
                    onClicked: {
                        contentLoader.source = "deletePage.qml"
                    }
                }
            }

            // Загрузчик для страниц
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Loader {
                    id: contentLoader
                    anchors.fill: parent
                    source: "viewPage.qml"
                }
            }
        }

        Component.onCompleted: {
            selectedAppsToAdd = []
            selectedAppsToRemove = []
        }

        Component.onDestruction: {
            selectedAppsToAdd = []
            selectedAppsToRemove = []
        }
    }
}
