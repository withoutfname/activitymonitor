import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "lightblue"

        RowLayout {
            anchors.fill: parent
            spacing: 10

            // Левая панель с кнопками навигации
            ColumnLayout {
                Layout.alignment: Qt.AlignTop | Qt.AlignLeft
                Layout.preferredWidth: 200 // Ширина левой панели
                spacing: 10

                Button {
                    text: "Запущенные приложения"
                    onClicked: loader.source = "runningAppsPage.qml"
                    Layout.preferredWidth: parent.width // Ширина кнопки равна ширине ColumnLayout
                    Layout.alignment: Qt.AlignTop // Выравнивание по верхнему краю
                }

                Button {
                    text: "Стандартные приложения"
                    onClicked: loader.source = "standartAppsPage.qml"
                    Layout.preferredWidth: parent.width // Ширина кнопки равна ширине ColumnLayout
                    Layout.alignment: Qt.AlignTop // Выравнивание по верхнему краю
                }

                Button {
                    text: "Пользовательские приложения"
                    onClicked: loader.source = "customAppsPage.qml"
                    Layout.preferredWidth: parent.width // Ширина кнопки равна ширине ColumnLayout
                    Layout.alignment: Qt.AlignTop // Выравнивание по верхнему краю
                }
            }

            // Правая часть с Loader для загрузки страниц
            Loader {
                id: loader
                Layout.fillWidth: true
                Layout.fillHeight: true
                source: "runningAppsPage.qml" // Загружаем первую страницу по умолчанию
            }
        }
    }


}