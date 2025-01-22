import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 1280
    height: 720
    minimumWidth: 1280
    minimumHeight: 720
    title: "Activity Monitor"
    color: "#F5F5F5"  // Светлый фон для всего окна

    // Основной макет
    RowLayout {
        anchors.fill: parent
        spacing: 0  // Убираем отступы между элементами

        // Панель навигации
        Rectangle {
            width: 200
            Layout.fillHeight: true
            color: "#FFFFFF"  // Белый фон для панели навигации
            border.color: "#E0E0E0"  // Серая граница

            ListView {
                id: navigation
                anchors.fill: parent
                anchors.margins: 10
                spacing: 5  // Отступ между элементами навигации
                clip: true  // Обрезаем содержимое, если оно выходит за пределы

                model: ListModel {
                    ListElement { name: "Главная"; file: "main.qml" }
                    ListElement { name: "Конфигурация"; file: "config.qml" }
                    ListElement { name: "Статистика"; file: "stats.qml" }
                }

                delegate: Item {
                    width: parent.width
                    height: 40  // Высота кнопки навигации

                    Button {
                        anchors.fill: parent
                        text: model.name
                        flat: true  // Убираем фон кнопки
                        font.pixelSize: 14
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.down ? "#0078D7" : "#333333"  // Цвет текста
                            horizontalAlignment: Text.AlignLeft
                            leftPadding: 10  // Отступ текста слева
                        }
                        background: Rectangle {
                            color: parent.hovered ? "#F0F0F0" : "transparent"  // Подсветка при наведении
                            radius: 5  // Скругление углов
                        }
                        onClicked: {
                            contentLoader.source = model.file  // Загружаем страницу
                        }
                    }
                }
            }
        }

        // Основная область контента
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#FFFFFF"  // Белый фон для контента
            border.color: "#E0E0E0"  // Серая граница

            Loader {
                id: contentLoader
                anchors.fill: parent
                anchors.margins: 10
                source: "main.qml"  // Начальная страница
            }
        }
    }
}