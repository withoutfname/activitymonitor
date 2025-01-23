import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        // Кнопка "Обновить"
        Button {
            text: "Обновить"
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
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
            onClicked: {
                updateStats();  // Обновляем статистику и текущие активности
            }
        }

        // Текущие активности
        Rectangle {
            width: parent.width
            height: 100
            color: "#1E1E1E"  // Темный фон
            radius: 10  // Скругление углов
            border.color: "#333333"  // Темная граница

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 5

                Text {
                    text: "Текущие активности:"
                    font.pixelSize: 16
                    color: "#E0E0E0"  // Светло-серый цвет текста
                    Layout.alignment: Qt.AlignHCenter
                }

                ListView {
                    width: parent.width
                    height: 60
                    model: ListModel {
                        id: incompleteActivitiesModel
                    }

                    delegate: Text {
                        text: name + " (начато: " + start_time + ", длительность: " + formatDuration(current_duration) + ")"
                        font.pixelSize: 14
                        color: "#E0E0E0"  // Светло-серый цвет текста
                    }
                }
            }
        }

        // Список статистики
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ListModel {
                id: statsModel
            }

            delegate: Item {
                width: ListView.view.width
                height: 50

                Rectangle {
                    width: parent.width
                    height: 50
                    color: "lightgray"
                    border.color: "gray"

                    Row {
                        anchors.fill: parent
                        spacing: 10
                        leftPadding: 10

                        Text {
                            text: name  // Название приложения
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            height: parent.height
                        }

                        Text {
                            text: exePath  // Путь к исполняемому файлу
                            font.pixelSize: 12
                            verticalAlignment: Text.AlignVCenter
                            height: parent.height
                        }

                        Text {
                            text: formatDuration(totalDuration)  // Общее время работы
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            height: parent.height
                        }
                    }
                }
            }
        }
    }

    // Функция для форматирования времени (секунды -> часы:минуты:секунды)
    function formatDuration(duration) {
        const hours = Math.floor(duration / 3600);
        const minutes = Math.floor((duration % 3600) / 60);
        const seconds = duration % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    // Инициализация данных при загрузке страницы
    Component.onCompleted: {
        updateStats();  // Обновляем данные при загрузке страницы
    }

    // Функция для обновления статистики и текущих активностей
    function updateStats() {
        // Обновляем статистику
        const stats = databaseManager.getAppStats();
        statsModel.clear();
        for (const stat of stats) {
            statsModel.append({
                name: stat.name,
                exePath: stat.exePath,
                totalDuration: stat.totalDuration
            });
        }

        // Обновляем текущие активности
        updateIncompleteActivities();
    }

    // Функция для обновления текущих активностей
    function updateIncompleteActivities() {
        const incompleteActivities = appMonitorManager.getIncompleteActivities();  // Используем appMonitorManager
        incompleteActivitiesModel.clear();
        for (const activity of incompleteActivities) {
            incompleteActivitiesModel.append({
                name: activity.name,
                start_time: activity.start_time,
                current_duration: activity.current_duration
            });
        }
    }
}