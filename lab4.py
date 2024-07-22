import os
import csv
import datetime


def set_attributes(obj, attributes):
    for key, value in attributes.items():
        if isinstance(obj, dict):
            obj[key] = value
        else:
            setattr(obj, key, value)


class DataProcessor:
    def __init__(self, directory_path, filename, new_filename):
        self.filename = filename
        self.sorted_by_name = None
        self.sorted_by_m = None
        self.filtered_data = None
        self.new_filename = new_filename
        self.data = []
        self.directory_path = directory_path
        set_attributes(self, locals())
        self.file_count = 0

    def __iter__(self):
        """Возвращает итератор для данных об осадках."""
        self.current_index = 0
        return self

    def __next__(self):
        """Возвращает следующий элемент данных об осадках."""
        if self.current_index >= len(self.data):
            raise StopIteration
        result = self.data[self.current_index]
        self.current_index += 1
        return result

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f"DataProcessor(data={self.data})"

    def __getitem__(self, index):
        """Возвращает элемент данных об осадках по индексу."""
        return self.data[index]

    @staticmethod
    def sort_by_date(data):
        """Сортирует данные по дате."""
        return sorted(data, key=lambda x: datetime.datetime.strptime(x['дата'], '%d.%m.%Y'))

    def count_files(self):
        for item in os.listdir(self.directory_path):
            item_path = os.path.join(self.directory_path, item)
            if os.path.isfile(item_path):
                self.file_count += 1
        print(f"Количество файлов в директории '{self.directory_path}': {self.file_count}")

    def read_precipitation_data(self):
        self.data = []
        for row in self.csv_reader(self.filename):  # Используем генератор
            try:
                set_attributes(row, {
                    '№': int(row['№']),
                    'дата': row['дата'],
                    'ФИО студента': (row['ФИО студента']),
                    'размер стипендии': int(row['размер стипендии']),
                    'куда выдается справка': (row['куда выдается справка']),
                })
                self.data.append(row)
            except ValueError as e:
                print(f"Пропущен некорректный ряд: {row}. Ошибка: {e}")

    def csv_reader(self, filename):
        """Генератор для чтения данных из CSV файла."""
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                yield row

    def print_data(self, data):
        for row in data:
            print(row)

    def save_precipitation_data(self, filename, data):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def process_data(self):
        self.read_precipitation_data()

        set_attributes(self, {
            'sorted_by_name': sorted(self.data, key=lambda x: x["ФИО студента"].split()[1]),
            'sorted_by_m': sorted(self.data, key=lambda x: int(x["размер стипендии"]), reverse=True),
            'filtered_data': [row for row in self.data if int(row["размер стипендии"]) > 4000]
        })

        print("Сортировка по ФИО:")
        self.print_data(self.sorted_by_name)

        print("Сортировка по размеру стипендии:")
        self.print_data(self.sorted_by_m)

        print("Суденты со стипендией больше 4000:")
        self.print_data(self.filtered_data)

        processed_data = {
            "Сортировка по ФИО": self.sorted_by_name,
            "Сортировка по размеру стипендии": self.sorted_by_m,
            "Суденты со стипендией больше 4000": self.filtered_data
        }

        with open(self.new_filename, 'w', newline='', encoding='utf-8') as csvfile:
            for title, data in processed_data.items():
                csvfile.write(f"{title}\n")
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys() if data else [])
                writer.writeheader()
                writer.writerows(data)
        print(f"Новые данные сохранены в файл '{self.new_filename}'")


class ScholarshipFilter(DataProcessor):
    def __init__(self, directory_path, filename, new_filename, min_scholarship, max_scholarship):
        super().__init__(directory_path, filename, new_filename)
        self.min_scholarship = min_scholarship
        self.max_scholarship = max_scholarship

    def process_data(self):
        super().process_data()
        self.filtered_data = [row for row in self.data
                              if self.min_scholarship <= int(row["размер стипендии"]) <= self.max_scholarship]

        print(f"Суденты со стипендией от {self.min_scholarship} до {self.max_scholarship}:")
        self.print_data(self.filtered_data)

        processed_data = {
            "Сортировка по ФИО": self.sorted_by_name,
            "Сортировка по размеру стипендии": self.sorted_by_m,
            f"Суденты со стипендией от {self.min_scholarship} до {self.max_scholarship}": self.filtered_data
        }

        with open(self.new_filename, 'w', newline='', encoding='utf-8') as csvfile:
            for title, data in processed_data.items():
                csvfile.write(f"{title}\n")
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys() if data else [])
                writer.writeheader()
                writer.writerows(data)
        print(f"Новые данные сохранены в файл '{self.new_filename}'")


if __name__ == "__main__":
    processor = ScholarshipFilter("C:\\Users\\ramis\\PycharmProjects\\Lab4\\data",
                                  "C:\\Users\\ramis\\PycharmProjects\\Lab4\\data\\data.csv",
                                  "C:\\Users\\ramis\\PycharmProjects\\Lab4\\data\\processed_data2.csv",
                                  3000, 5000)
    processor.count_files()
    processor.process_data()
