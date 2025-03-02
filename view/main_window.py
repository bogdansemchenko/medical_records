from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMenuBar, QAction, QToolBar, QMessageBox,
    QHBoxLayout, QLabel, QSpinBox, QPushButton, QFileDialog, QHeaderView
)
from view.add_dialog import AddRecordDialog
from view.search_dialog import SearchDialog
from view.delete_dialog import DeleteDialog
from view.tree_view_dialog import TreeViewDialog
from controller.controller import Controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Медицинские записи")
        self.setGeometry(100, 100, 1200, 600)  # Увеличиваем размер окна

        self.controller = Controller()

        # Таблица для отображения записей
        self.table = QTableWidget(self)
        self.setup_table()  # Настраиваем таблицу (ширину колонок и заголовки)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Пагинация
        self.page_size = 10
        self.current_page = 1
        self.total_records = 0

        self.pagination_layout = QHBoxLayout()
        self.page_label = QLabel("Страница: 1", self)
        self.page_size_input = QSpinBox(self)
        self.page_size_input.setMinimum(1)
        self.page_size_input.setValue(10)
        self.page_size_input.valueChanged.connect(self.change_page_size)
        self.prev_button = QPushButton("Предыдущая", self)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Следующая", self)
        self.next_button.clicked.connect(self.next_page)

        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(QLabel("Записей на странице:"))
        self.pagination_layout.addWidget(self.page_size_input)
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.next_button)

        # Кнопка возврата к общему списку
        self.reset_button = QPushButton("Вернуться к общему списку", self)
        self.reset_button.clicked.connect(self.load_records)
        self.reset_button.setVisible(False)  # Скрыта по умолчанию

        layout.addLayout(self.pagination_layout)
        layout.addWidget(self.reset_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_tool_bar()  # Создаем панель инструментов с кнопками
        self.load_records()

    def setup_table(self):
        """Настраивает таблицу: заголовки и ширину колонок."""
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ФИО", "Адрес", "Дата рождения", "Дата приема", "ФИО врача", "Заключение"])

        # Устанавливаем ширину колонок
        self.table.setColumnWidth(0, 200)  # ФИО
        self.table.setColumnWidth(1, 250)  # Адрес
        self.table.setColumnWidth(2, 120)  # Дата рождения
        self.table.setColumnWidth(3, 120)  # Дата приема
        self.table.setColumnWidth(4, 200)  # ФИО врача
        self.table.setColumnWidth(5, 300)  # Заключение

        # Настройка растягивания колонок по содержимому
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def create_tool_bar(self):
        """Создает панель инструментов с кнопками."""
        tool_bar = self.addToolBar("Инструменты")

        # Кнопка "Добавить"
        add_action = QAction("Добавить", self)
        add_action.triggered.connect(self.show_add_dialog)
        tool_bar.addAction(add_action)

        # Кнопка "Поиск"
        search_action = QAction("Поиск", self)
        search_action.triggered.connect(self.show_search_dialog)
        tool_bar.addAction(search_action)

        # Кнопка "Удалить"
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.show_delete_dialog)
        tool_bar.addAction(delete_action)

        # Кнопка "Дерево"
        tree_view_action = QAction("Дерево", self)
        tree_view_action.triggered.connect(self.show_tree_view_dialog)
        tool_bar.addAction(tree_view_action)

        # Кнопка "Сохранить в XML"
        save_action = QAction("Сохранить в XML", self)
        save_action.triggered.connect(self.save_to_xml)
        tool_bar.addAction(save_action)

        # Кнопка "Загрузить из XML"
        load_action = QAction("Загрузить из XML", self)
        load_action.triggered.connect(self.load_from_xml)
        tool_bar.addAction(load_action)

    def load_records(self):
        """Загружает записи из базы данных и отображает их в таблице."""
        self.total_records = len(self.controller.get_all_records())
        records = self.controller.get_all_records()
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        paginated_records = records[start:end]

        self.table.setRowCount(len(paginated_records))
        for i, record in enumerate(paginated_records):
            self.table.setItem(i, 0, QTableWidgetItem(record[1]))  # ФИО
            self.table.setItem(i, 1, QTableWidgetItem(record[2]))  # Адрес
            self.table.setItem(i, 2, QTableWidgetItem(record[3]))  # Дата рождения
            self.table.setItem(i, 3, QTableWidgetItem(record[4]))  # Дата приема
            self.table.setItem(i, 4, QTableWidgetItem(record[5]))  # ФИО врача
            self.table.setItem(i, 5, QTableWidgetItem(record[6]))  # Заключение

        self.update_pagination_labels()
        self.reset_button.setVisible(False)  # Скрываем кнопку возврата

    def update_pagination_labels(self):
        """Обновляет метки пагинации."""
        total_pages = (self.total_records + self.page_size - 1) // self.page_size
        self.page_label.setText(f"Страница: {self.current_page} из {total_pages}")
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)

    def change_page_size(self):
        """Изменяет количество записей на странице."""
        self.page_size = self.page_size_input.value()
        self.current_page = 1
        self.load_records()

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_records()

    def next_page(self):
        """Переход на следующую страницу."""
        total_pages = (self.total_records + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_records()

    def show_add_dialog(self):
        """Открывает диалог добавления записи."""
        dialog = AddRecordDialog(self)
        if dialog.exec_():
            record = dialog.get_record()
            self.controller.add_record(record)
            self.load_records()

    def show_search_dialog(self):
        """Открывает диалог поиска записей."""
        dialog = SearchDialog(self)
        if dialog.exec_():
            conditions = dialog.get_conditions()
            records = self.controller.search_records(conditions)
            if records:
                self.display_search_results(records)
                self.reset_button.setVisible(True)  # Показываем кнопку возврата
            else:
                QMessageBox.information(self, "Поиск", "Записи не найдены.")

    def show_delete_dialog(self):
        """Открывает диалог удаления записей."""
        dialog = DeleteDialog(self)
        if dialog.exec_():
            conditions = dialog.get_conditions()
            deleted_count = self.controller.delete_records(conditions)
            if deleted_count > 0:
                QMessageBox.information(self, "Удаление", f"Удалено записей: {deleted_count}")
            else:
                QMessageBox.information(self, "Удаление", "Записи не найдены.")
            self.load_records()

    def show_tree_view_dialog(self):
        """Открывает диалог отображения данных в виде дерева."""
        records = self.controller.get_all_records()
        dialog = TreeViewDialog(records, self)
        dialog.exec_()

    def save_to_xml(self):
        """Сохраняет данные в XML-файл."""
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить в XML", "", "XML Files (*.xml)")
        if filename:
            self.controller.save_to_xml(filename)

    def load_from_xml(self):
        """Загружает данные из XML-файла."""
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить из XML", "", "XML Files (*.xml)")
        if filename:
            self.controller.load_from_xml(filename)
            self.load_records()

    def display_search_results(self, records):
        """Отображает результаты поиска в таблице."""
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record[1]))  # ФИО
            self.table.setItem(i, 1, QTableWidgetItem(record[2]))  # Адрес
            self.table.setItem(i, 2, QTableWidgetItem(record[3]))  # Дата рождения
            self.table.setItem(i, 3, QTableWidgetItem(record[4]))  # Дата приема
            self.table.setItem(i, 4, QTableWidgetItem(record[5]))  # ФИО врача
            self.table.setItem(i, 5, QTableWidgetItem(record[6]))  # Заключение