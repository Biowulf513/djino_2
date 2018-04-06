# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"
'''
План действий:

1. С какого ящика и сколько писем было отправлено:
    1.1 Построчное чтение файла
    1.2 Проверка строки на наличие message_id
        1.2.1 Если message_id встречается впервые создаём словарь или 
            добавляем данные в уже существующий словарь
        1.2.2 Наличие в строке 2х message_id обозначает провал доставки 
            второй message_id - сообщение об ошибке (игнорируем его)
            1.2.2.1 Удаляем словарь второго message_id 
    1.3 Поочерёдно парсим словари 
        1.3.1 Наличие в словаре строки 'removed' обозначает окончание 
        работы с данным сообщением (передаём сообщение в обработку)
    1.4 Находим в списке словаря значения (from, status)
        1.4.1 Приводим значения в общий вид (access, denied)
    1.5 Производим действия со значениями подобно пункту 2.1
    1.6 Производим подсчёт значений в списках из пункта 5

2. Сколько писем отправлено успешно и сколько с ошибками:
    2.1. Производим подсчёт конкретных значений подобно пункту 1.6

3. Результат обработки представить в виде таблицы или отчета. 
    Сохраним конечные данные используя CSV
'''
import re

class LogParser():
    reg_exp = {'message_id':r':\s+([0-9A-Z]{11})\W'}

    def __init__(self, filename):
        self.filename = filename

    def read_log(self):
        with open(self.filename, mode='r') as f:
            for line in f:
                message_id = re.findall(self.reg_exp['message_id'], line)
                if message_id:
                    self.log_line_analise(message_id, line)

    def log_line_analise(self, message_id, line):
        pass

if __name__ == '__main__':
    parse = LogParser('maillog')
    parse.read_log()

