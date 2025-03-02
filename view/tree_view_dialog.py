from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem

class TreeViewDialog(QDialog):
    def __init__(self, records, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Дерево записей")
        self.setGeometry(100, 100, 600, 400)  # Увеличиваем размер окна
        layout = QVBoxLayout()

        # Создаем дерево
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Поле", "Значение"])
        layout.addWidget(self.tree)

        # Группируем записи по первой букве ФИО
        grouped_records = self.group_records_by_initial(records)

        # Добавляем записи в дерево
        for initial, group in grouped_records.items():
            # Создаем корневой элемент для группы
            group_item = QTreeWidgetItem(self.tree)
            group_item.setText(0, f"Группа '{initial}'")

            # Добавляем записи в группу
            for record in group:
                record_item = QTreeWidgetItem(group_item)
                record_item.setText(0, f"Запись {group.index(record) + 1}")

                # Добавляем поля записи как дочерние элементы
                headers = ["ФИО", "Адрес", "Дата рождения", "Дата приема", "ФИО врача", "Заключение"]
                for key, value in zip(headers, record[1:]):  # Пропускаем ID
                    field_item = QTreeWidgetItem(record_item)
                    field_item.setText(0, key)
                    field_item.setText(1, str(value))

        # Раскрываем все узлы для удобства просмотра
        self.tree.expandAll()

        self.setLayout(layout)

    def group_records_by_initial(self, records):
        """
        Группирует записи по первой букве ФИО.
        """
        grouped = {}
        for record in records:
            fio = record[1]  # ФИО находится на втором месте (после ID)
            initial = fio[0].upper()  # Первая буква ФИО
            if initial not in grouped:
                grouped[initial] = []
            grouped[initial].append(record)
        return grouped