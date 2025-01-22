import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    // Инициализация массивов для временного хранения отмеченных приложений
    property var runningAppsToAdd: [] // Для страницы "Запущенные приложения"

    Rectangle {
        anchors.fill: parent
        color: "#121212"  // Темный фон (почти черный)

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

                    // Стилизация кнопки
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "#FFFFFF"  // Белый цвет текста
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    background: Rectangle {
                        color: parent.down ? "#005BB5" : "#0078D7"  // Синий цвет кнопки
                        radius: 5  // Скругление углов
                    }
                }

                // Кнопка "Скоро"
                Button {
                    text: "Скоро"
                    enabled: false // Делаем кнопку некликабельной
                    Layout.preferredWidth: parent.width
                    Layout.alignment: Qt.AlignTop

                    // Стилизация кнопки
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "#808080"  // Серый цвет текста (для некликабельной кнопки)
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    background: Rectangle {
                        color: "#333333"  // Темно-серый цвет фона
                        radius: 5  // Скругление углов
                    }

                    // Обработка клика (несмотря на то, что кнопка некликабельна)
                    onClicked: {
                        loader.source = "customAppsPage.qml" // Загружаем empty.qml
                    }
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