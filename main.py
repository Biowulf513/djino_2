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
import re, csv

class LogParser():
    reg_exp = {'message_id':r':\s+([0-9A-Z]{11})\W'}
    notification = []
    all_log_messages = {}

    def __init__(self, filename):
        self.filename = filename

    # Чиатем данные из файла, передаём информацию о сообщениях в обработку
    def read_log(self):
        with open(self.filename, mode='r') as f:
            for line in f:
                id = re.findall(self.reg_exp['message_id'], line)
                if id:
                    self.log_line_parsing(dict(id = id, text = line.rstrip()))

    # Разбераем словари
    def log_line_parsing(self, message):
        if len(message['id']) > 1 :
            self.notification.append(message['id'].pop(1))

        message['id'] = message['id'][0]
        self.check_record_in_dict(message)

    # Проверяем существует ли информация с таким-же id
    def check_record_in_dict(self, message):
        # Если id уникален создаём новую запись
        if self.all_log_messages.get(message['id']):
            self.all_log_messages[message['id']].append(message['text'])
        # Если id уже есть добовляем информацию к существующей
        else:
            self.all_log_messages.update({message['id']:[message['text']]})

    # Убираем из notification все записи с нормальными письмами
    def clear_all_log_messages(self):
        for record in self.notification:
            self.all_log_messages.pop(record)

class RecordsParser:
    reg_exp = {'sender':r'from=<(\S+)>', 'status':r'status=(\w+)'}
    all_sender = {}
    sum_sender = {}

    def __init__(self):
        self.all_records = LogParser.all_log_messages

    # Если в списке присутствует строчка removed, процес/попытка отправки окончена, приступаем к обработке
    def is_message_over(self):
        for one_message in self.all_records:
            if re.search(r'removed\b',self.all_records[one_message][-1]):
                self.find_sender_and_status(self.all_records[one_message])

    # Находим отправителя и статус отправки
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

    # Добавляем информацию в словарь
    def add_info_to_dict(self, info):
        if info['sender'] in self.all_sender:
            self.all_sender[info['sender']].append(info['status'])
        else:
            self.all_sender.update({info['sender']:[info['status']]})

    def collect_sender_messages_info(self):
        for sender in self.all_sender:
            if sender not in self.sum_sender:
                self.sum_sender[sender] = {'access':0, 'denied':0}
            for status in self.all_sender[sender]:
                self.sum_sender[sender][status] += 1

    def sum_sender_messages_info(self):
        for sender in self.sum_sender:
            self.sum_sender[sender]['message_col'] = self.sum_sender[sender]['access'] + self.sum_sender[sender]['denied']

class CSV_convector:
    def __init__(self):
        self.sender_statistics = RecordsParser.sum_sender

    def export_sender_stat(self, sender_statistics=None):
        filename = 'statistics.csv'

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            header = ['sender_email', 'access', 'denied', 'sum_messages']
            writer.writerow(header)

            for sender in sender_statistics:
                writer.writerow((sender,
                                 sender_statistics[sender]['access'],
                                 sender_statistics[sender]['denied'],
                                 sender_statistics[sender]['message_col']))

if __name__ == '__main__':
    log = LogParser('maillog')
    log.read_log()
    log.clear_all_log_messages()

    message_info = RecordsParser()
    message_info.is_message_over()
    message_info.collect_sender_messages_info()

    for record in message_info.sum_sender:
        print(record, end=' | ')


    # output_csv = CSV_convector()
    # output_csv.export_sender_stat()









