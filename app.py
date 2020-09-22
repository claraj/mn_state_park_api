import json
import sqlite3
from flask import Flask 
from flask.json import jsonify
from flask import abort


app = Flask(__name__)

db = 'park.db'

@app.route('/api/list')
def send_park_list():

    con = sqlite3.connect(db)
    data = con.execute('SELECT park_id, name FROM parks ORDER BY park_id')
    parks = [ { 'park_id': row[0], 'name': row[1]} for row in data ]
    con.close()
    return jsonify(parks)


@app.route('/api/<park_id>')
def send_park(park_id):
    if len(park_id) < 5:
        park_id = park_id.zfill(5)

    con = sqlite3.connect(db)
    data = con.execute('SELECT json FROM parks WHERE park_id = ?', (park_id,) ).fetchone()
    if data:
        park_json = data[0]
        park_info = json.loads(park_json)
        return park_info
    else:
        abort(404, f'Park with id {park_id} not found')


@app.errorhandler(404)
def not_found(e):
    return 'Not found'