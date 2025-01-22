import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    // Инициализация массивов для временного хранения отмеченных приложений
    property var runningAppsToAdd: [] // Для страницы "Запущенные приложения"

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
                    onClicked: {
                        // Очищаем массив перед загрузкой страницы
                        runningAppsToAdd = []
                        loader.source = "runningAppsPage.qml"
                        loader.item.runningAppsToAdd = runningAppsToAdd // Передаем массив
                    }
                    Layout.preferredWidth: parent.width
                    Layout.alignment: Qt.AlignTop
                }
            }

            // Правая часть с Loader для загрузки страниц
            Loader {
                id: loader
                Layout.fillWidth: true
                Layout.fillHeight: true
                source: "runningAppsPage.qml" // Загружаем первую страницу по умолчанию
                onLoaded: {
                    if (source === "runningAppsPage.qml") {
                        item.runningAppsToAdd = runningAppsToAdd // Передаем массив при загрузке

                    }
                }
            }
        }
    }
}