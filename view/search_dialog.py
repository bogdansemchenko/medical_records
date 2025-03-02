from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from dateutil.parser import parse
from dateutil.parser import ParserError

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск записей")
        layout = QVBoxLayout()

        # Валидатор для ФИО (только буквы, пробелы и дефисы)
        name_validator = QRegExpValidator(QRegExp("[а-яА-ЯёЁa-zA-Z\\s-]+"), self)

        # ФИО пациента
        self.fio_input = QLineEdit(self)
        self.fio_input.setPlaceholderText("ФИО пациента")
        self.fio_input.setValidator(name_validator)  # Устанавливаем валидатор
        layout.addWidget(QLabel("ФИО пациента"))
        layout.addWidget(self.fio_input)

        # Адрес прописки
        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Адрес прописки")
        layout.addWidget(QLabel("Адрес прописки"))
        layout.addWidget(self.address_input)

        # Дата рождения (QLineEdit)
        self.birth_date_input = QLineEdit(self)
        self.birth_date_input.setPlaceholderText("дд.мм.гггг")
        layout.addWidget(QLabel("Дата рождения"))
        layout.addWidget(self.birth_date_input)

        # Дата приема (QLineEdit)
        self.appointment_date_input = QLineEdit(self)
        self.appointment_date_input.setPlaceholderText("дд.мм.гггг")
        layout.addWidget(QLabel("Дата приема"))
        layout.addWidget(self.appointment_date_input)

        # ФИО врача
        self.doctor_fio_input = QLineEdit(self)
        self.doctor_fio_input.setPlaceholderText("ФИО врача")
        self.doctor_fio_input.setValidator(name_validator)  # Устанавливаем валидатор
        layout.addWidget(QLabel("ФИО врача"))
        layout.addWidget(self.doctor_fio_input)

        # Кнопка поиска
        self.search_button = QPushButton("Поиск", self)
        self.search_button.clicked.connect(self.accept)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def get_conditions(self):
        conditions = {}
        if self.fio_input.text():
            conditions['fio'] = self.fio_input.text()
        if self.address_input.text():
            conditions['address'] = self.address_input.text()
        if self.birth_date_input.text():
            try:
                birth_date = parse(self.birth_date_input.text(), dayfirst=True)
                conditions['birth_date'] = birth_date.strftime("%d.%m.%Y")
            except ParserError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат даты рождения! Используйте дд.мм.гггг.")
                return {}
        if self.appointment_date_input.text():
            try:
                appointment_date = parse(self.appointment_date_input.text(), dayfirst=True)
                conditions['appointment_date'] = appointment_date.strftime("%d.%m.%Y")
            except ParserError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат даты приема! Используйте дд.мм.гггг.")
                return {}
        if self.doctor_fio_input.text():
            conditions['doctor_fio'] = self.doctor_fio_input.text()
        return conditions