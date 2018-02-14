import csv
import json
from server.storage import Storage


class FileStorage(Storage):
    """ Файловое хранилище, в формате CSV"""
    def __init__(self, filename):
        self.filename = filename

    def add(self, table, key, data):
        print(data)
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=':', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([table, key, json.dumps(data)])
