import csv
import os

'''
Пусть дана некоторая директория (папка). Посчитайте количество файлов в данной директории (папке) и выведите на экран.

Пусть дан файл data.csv, в котором содержится информация в соответствии с вариантом:

Считайте информацию из файла в соответствующую структуру (словарь):

2.1. Выведите информацию об объектах, отсортировав их по одному полю (строковому).

2.2. Выведите информацию об объектах, отсортировав их по одному полю (числовому).

2.3. Выведите информацию, соответствующую какому-либо критерию
(например, для студентов - тех, у кого возраст больше какого-либо значения)

Добавьте к программе возможность сохранения новых данных обратно в файл.
'''

# указывается путь к директории
directory = r"C:\Users\ramis\PycharmProjects\Lab3\data"
# Считаем колличество файлов
files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
print("1.Количество файлов в директории:", files)


def read_csv_file(file_path_local):
    # функция считывает данные из файла и возвращает в форме списка словарей
    data = []
    with open(file_path_local, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
    return data


def print_data(data_list_local):
    # функция вывода информации из списка словарей
    for row in data_list_local:
        print(row)


def write_csv(file_path_local, data):
    # функция для записи данных из списка словарей в новый CSV файл
    with open(file_path_local, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)


file_path = r"C:\Users\ramis\PycharmProjects\Lab3\data\data.csv"
data_list = read_csv_file(file_path)

sorted_data1 = sorted(data_list, key=lambda x: int(x["размер стипендии"]), reverse=True)
print('\n', '2.1.Сортировка по размеру стипендии:')
print_data(sorted_data1)

sorted_data2 = sorted(data_list, key=lambda x: x["ФИО студента"].split()[1])
print('\n', '2.2.Сортировка по ФИО:')
print_data(sorted_data2)

filtered_data = [row for row in data_list if int(row["размер стипендии"]) > 4000]
print('\n', '2.3.Суденты со стипендией больше 4000:')
print_data(filtered_data)

new_file = os.path.join(os.path.dirname(file_path), 'filtered.csv')
write_csv(new_file, filtered_data)
