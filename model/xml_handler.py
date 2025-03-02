import xml.etree.ElementTree as ET
from xml.sax import make_parser, handler

class DOMHandler:
    @staticmethod
    def save_to_xml(records, filename):
        """
        Сохраняет список записей в XML-файл с отступами и поддержкой русских символов.

        :param records: Список записей (каждая запись — это кортеж или список).
        :param filename: Имя файла для сохранения.
        """
        try:
            # Создаем корневой элемент
            root = ET.Element("records")

            # Проходим по всем записям и добавляем их в XML
            for record in records:
                record_elem = ET.SubElement(root, "record")

                # Добавляем поля записи
                ET.SubElement(record_elem, "fio").text = record[1]  # ФИО
                ET.SubElement(record_elem, "address").text = record[2]  # Адрес
                ET.SubElement(record_elem, "birth_date").text = record[3]  # Дата рождения
                ET.SubElement(record_elem, "appointment_date").text = record[4]  # Дата приема
                ET.SubElement(record_elem, "doctor_fio").text = record[5]  # ФИО врача
                ET.SubElement(record_elem, "conclusion").text = record[6]  # Заключение

            # Создаем XML-дерево
            tree = ET.ElementTree(root)

            # Добавляем отступы для красивого форматирования
            ET.indent(tree, space="\t", level=0)

            # Записываем XML в файл с поддержкой русских символов
            tree.write(filename, encoding="utf-8", xml_declaration=True)
            print(f"Данные успешно сохранены в файл: {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении в XML: {e}")

    @staticmethod
    def load_from_xml(filename):
        """
        Загружает данные из XML-файла.

        :param filename: Имя файла для загрузки.
        :return: Список записей.
        """
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            records = []
            for record_elem in root.findall('record'):
                record = {
                    "fio": record_elem.find('fio').text,
                    "address": record_elem.find('address').text,
                    "birth_date": record_elem.find('birth_date').text,
                    "appointment_date": record_elem.find('appointment_date').text,
                    "doctor_fio": record_elem.find('doctor_fio').text,
                    "conclusion": record_elem.find('conclusion').text
                }
                records.append(record)
            return records
        except Exception as e:
            print(f"Ошибка при загрузке XML: {e}")
            return []

class SAXHandler(handler.ContentHandler):
    def __init__(self):
        self.records = []
        self.current_record = {}
        self.current_element = ""

    def startElement(self, name, attrs):
        self.current_element = name

    def characters(self, content):
        if self.current_element:
            self.current_record[self.current_element] = content

    def endElement(self, name):
        if name == "record":
            self.records.append(self.current_record)
            self.current_record = {}
        self.current_element = ""

    @staticmethod
    def load_from_xml(filename):
        parser = make_parser()
        handler = SAXHandler()
        parser.setContentHandler(handler)
        parser.parse(filename)
        return handler.records