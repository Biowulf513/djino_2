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
        1.2.2 Второй message_id в строке лога это уведомление(игнорируем его)
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
import re, time

class LogParser():
    reg_exp = {'message_id':r':\s+([0-9A-Z]{11})\W'}
    notification = []
    all_log_messages = {}

    def __init__(self, filename):
        self.filename = filename

    def read_log(self):
        with open(self.filename, mode='r') as f:
            for line in f:
                id = re.findall(self.reg_exp['message_id'], line)
                if id:
                    self.log_line_parsing(dict(id = id, text = line.rstrip()))

    def log_line_parsing(self, message):
        if len(message['id']) > 1 :
            self.notification.append(message['id'].pop(1))

        message['id'] = message['id'][0]
        self.check_record_in_dict(message)


    def check_record_in_dict(self, message):
        if self.all_log_messages.get(message['id']):
            self.all_log_messages[message['id']].append(message['text'])
        else:
            self.all_log_messages.update({message['id']:[message['text']]})

    def clear_all_log_messages(self):
        for record in self.notification:
            self.all_log_messages.pop(record)

class RecordsParser:
    reg_exp = {'sender':r'from=<(\S+)>', 'status':r'status=(\w+)'}
    all_sender = {}

    def __init__(self):
        self.all_records = LogParser.all_log_messages

    # Если в списке присутствует строчка removed, процес/попытка отправки окончена
    def is_message_over(self):
        for one_message in self.all_records:
            if re.search(r'removed\b',self.all_records[one_message][-1]):
                self.find_sender_and_status(self.all_records[one_message])

    def find_sender_and_status(self, record_dict):
        status_var = {'sent': 'access', 'expired': 'denied', 'bounced': 'denied', 'deferred': 'denied'}
        sender = None
        status = None

        for line in record_dict:
            found_sender = re.findall(self.reg_exp['sender'], line)
            if found_sender:
                sender = found_sender[0]

            found_status = re.findall(self.reg_exp['status'], line)
            if found_status:
                status = status_var[found_status[0]]

        self.add_info_to_dict({'sender':sender,'status':status})

    def add_info_to_dict(self, info):
        if info['sender'] in self.all_sender:
            self.all_sender[info['sender']].append(info['status'])
        else:
            self.all_sender.update({info['sender']:[info['status']]})

    def sum_sender_messages(self):
        for sender in self.all_sender:
            print(sender, len(self.all_sender[sender]))
            

if __name__ == '__main__':
    parse = LogParser('maillog')
    parse.read_log()
    parse.clear_all_log_messages()

    parse2 = RecordsParser()
    parse2.is_message_over()
    parse2.sum_sender_messages()


