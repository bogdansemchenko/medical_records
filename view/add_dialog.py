from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from dateutil.parser import parse
from dateutil.parser import ParserError

class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        layout = QVBoxLayout()

        # Валидатор для ФИО (только буквы, пробелы и дефисы)
        name_validator = QRegExpValidator(QRegExp("[а-яА-ЯёЁa-zA-Z\\s-]+"), self)

        # ФИО пациента
        self.fio_input = QLineEdit(self)
        self.fio_input.setPlaceholderText("ФИО пациента")
        self.fio_input.setValidator(name_validator)  # Устанавливаем валидатор
        layout.addWidget(QLabel("ФИО пациента (обязательно)"))
        layout.addWidget(self.fio_input)

        # Адрес прописки
        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Адрес прописки")
        layout.addWidget(QLabel("Адрес прописки (обязательно)"))
        layout.addWidget(self.address_input)

        # Дата рождения (QLineEdit)
        self.birth_date_input = QLineEdit(self)
        self.birth_date_input.setPlaceholderText("дд.мм.гггг")
        layout.addWidget(QLabel("Дата рождения (обязательно)"))
        layout.addWidget(self.birth_date_input)

        # Дата приема (QLineEdit)
        self.appointment_date_input = QLineEdit(self)
        self.appointment_date_input.setPlaceholderText("дд.мм.гггг")
        layout.addWidget(QLabel("Дата приема (обязательно)"))
        layout.addWidget(self.appointment_date_input)

        # ФИО врача
        self.doctor_fio_input = QLineEdit(self)
        self.doctor_fio_input.setPlaceholderText("ФИО врача")
        self.doctor_fio_input.setValidator(name_validator)  # Устанавливаем валидатор
        layout.addWidget(QLabel("ФИО врача (обязательно)"))
        layout.addWidget(self.doctor_fio_input)

        # Заключение
        self.conclusion_input = QLineEdit(self)
        self.conclusion_input.setPlaceholderText("Заключение")
        layout.addWidget(QLabel("Заключение (обязательно)"))
        layout.addWidget(self.conclusion_input)

        # Кнопка добавления
        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        # Проверка, что все поля заполнены
        if (not self.fio_input.text() or not self.address_input.text() or
            not self.birth_date_input.text() or
            not self.appointment_date_input.text() or
            not self.doctor_fio_input.text() or not self.conclusion_input.text()):
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка корректности даты рождения
        try:
            birth_date = parse(self.birth_date_input.text(), dayfirst=True)
        except ParserError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты рождения! Используйте дд.мм.гггг.")
            return

        # Проверка года рождения (1920–2024)
        birth_year = birth_date.year
        if birth_year < 1920 or birth_year > 2024:
            QMessageBox.warning(self, "Ошибка", "Год рождения должен быть в диапазоне от 1920 до 2024!")
            return

        # Проверка корректности даты приема
        try:
            appointment_date = parse(self.appointment_date_input.text(), dayfirst=True)
        except ParserError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты приема! Используйте дд.мм.гггг.")
            return

        # Проверка, что дата приема позже даты рождения
        if appointment_date <= birth_date:
            QMessageBox.warning(self, "Ошибка", "Дата приема должна быть позже даты рождения!")
            return

        # Если все проверки пройдены, закрываем диалог
        self.accept()

    def get_record(self):
        return {
            'fio': self.fio_input.text(),
            'address': self.address_input.text(),
            'birth_date': parse(self.birth_date_input.text(), dayfirst=True).strftime("%d.%m.%Y"),
            'appointment_date': parse(self.appointment_date_input.text(), dayfirst=True).strftime("%d.%m.%Y"),
            'doctor_fio': self.doctor_fio_input.text(),
            'conclusion': self.conclusion_input.text()
        }