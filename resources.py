from typing import List
import os, json

def print_with_indent(value, indent=0):
    print(('\t' * indent) + str(value))

class Entry:
    def __init__(self, title='', entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return f"{self.title}"

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': []
        }
        for entry in self.entries:
            res['entries'].append(entry.json())
        return res

    @classmethod
    def from_json(cls, values):
        new_enrty = cls(values['title'])
        for value in values.get('entries', []):
            new_enrty.add_entry(cls.from_json(value))
        return new_enrty

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w', encoding='utf-8') as f:
            value = json.dumps(self.json(), ensure_ascii=False)
            f.write(value)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return cls.from_json(content)


class EntryManager:
    def __init__(self, data_path):
        self.entries: List[Entry] = []
        self.data_path = data_path

    def save(self):
        for item in self.entries:
            file_path = os.path.join(self.data_path)
            item.save(file_path)

    def load(self):
        for file_name in os.listdir(self.data_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.data_path, file_name)
                entry = Entry.load(file_path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))