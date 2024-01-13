from flask import Flask, request
from resources import EntryManager
from resources import Entry

app = Flask(__name__)
FOLDER = 'D:/test'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries/")
def get_entries():
    entrylist = list()
    entryManager = EntryManager(FOLDER)
    entryManager.load()
    for entry in entryManager.entries:
        entrylist.append(entry.json())
    return entrylist

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    rjson = request.get_json()
    for r in rjson:
        entry = Entry.from_json(r)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)