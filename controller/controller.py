from model.database import Database
from model.xml_handler import DOMHandler, SAXHandler

class Controller:
    def __init__(self):
        self.database = Database()
        self.dom_handler = DOMHandler()
        self.sax_handler = SAXHandler()

    def add_record(self, record):
        """
        Добавляет запись в базу данных.

        :param record: Словарь с данными записи.
        """
        self.database.add_record(record)

    def search_records(self, conditions):
        """
        Ищет записи в базе данных по заданным условиям.

        :param conditions: Словарь с условиями поиска.
        :return: Список найденных записей.
        """
        return self.database.search_records(conditions)

    def delete_records(self, conditions):
        """
        Удаляет записи из базы данных по заданным условиям.

        :param conditions: Словарь с условиями удаления.
        :return: Количество удаленных записей.
        """
        return self.database.delete_records(conditions)

    def get_all_records(self):
        """
        Возвращает все записи из базы данных.

        :return: Список всех записей.
        """
        return self.database.get_all_records()

    def save_to_xml(self, filename):
        """
        Сохраняет все записи из базы данных в XML-файл.

        :param filename: Имя файла для сохранения.
        """
        records = self.database.get_all_records()
        self.dom_handler.save_to_xml(records, filename)

    def load_from_xml(self, filename):
        """
        Загружает записи из XML-файла в базу данных.

        :param filename: Имя файла для загрузки.
        """
        records = self.sax_handler.load_from_xml(filename)
        for record in records:
            # Проверяем, существует ли запись с такими же данными
            existing_records = self.database.search_records({
                "fio": record["fio"],
                "birth_date": record["birth_date"],
                "appointment_date": record["appointment_date"]
            })
            if not existing_records:  # Если дубликатов нет, добавляем запись
                self.database.add_record(record)