# -*- coding: utf-8 -*-

import re
from abc import abstractmethod


class Find_Mail_Info:
    reg_exp = {'message_id': r':\s+([0-9A-Z]{11})\W',
               'sender':r'from=<(\S+)>',
               'status':r'status=(\w+)'}

    def __init__(self, file_name):
        self.file = file_name

    @abstractmethod
    def read_log(self):
        with open(self.file, mode='r') as f:
            for line in f:
                mail_id = re.findall(self.reg_exp['message_id'], line)
                if mail_id:
                    yield {mail_id[0]:line}

    '''
    
    1.1 Построчное чтение файла
    1.2 Проверка строки на наличие message_id
        1.2.1 Если message_id встречается впервые создаём словарь или 
            добавляем данные в уже существующий словарь
        1.2.2 Второй message_id в строке лога это уведомление(игнорируем его)
            1.2.2.1 Удаляем словарь второго message_id 
    
    '''
    pass

class Message:
    message_array = []
    def __init__(self):
        self.message_array.append(Find_Mail_Info.read_log())

    def printer(self):
        for i in self.message_array:
            print(i)


    '''
    
    1.3 Поочерёдно парсим словари 
        1.3.1 Наличие в словаре строки 'removed' обозначает окончание 
        работы с данным сообщением (передаём сообщение в обработку)
    1.4 Находим в списке словаря значения (from, status)
        1.4.1 Приводим значения в общий вид (access, denied)
    1.5 Производим действия со значениями подобно пункту 2.1
    
    '''

    pass

class Messages_Statistic:
    '''
    
        1.6 Производим подсчёт значений в списках из пункта 5

    2. Сколько писем отправлено успешно и сколько с ошибками:
        2.1. Производим подсчёт конкретных значений подобно пункту 1.6
    
    '''

    pass
class Parser:
    def __init__(self):
        test = Find_Mail_Info('maillog')
        i = Message()
        i.

class CSV_Convector:
    '''
    
    3. Результат обработки представить в виде таблицы или отчета. 
    Сохраним конечные данные используя CSV
    
    '''
    pass

if __name__ == '__main__':
    parser_one = Parser()

