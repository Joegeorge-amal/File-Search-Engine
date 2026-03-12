import os 
import subprocess
import sys
from flask import Flask, request, jsonify, send_from_directory
import threading
import watcher
import database

app = Flask(__name__,static_folder = 'static')
database.create()

@app.route('/')
def index():
    return send_from_directory('static','index.html')

@app.route('/api/search')
def search():
    query = request.args.get('q','').strip()
    if not query:
        return jsonify([])
    results = database.search(query)
    return jsonify(results)

@app.route('/api/open')
def open_file():
    path = request.args.get('path','')
    if not path or not os.path.exists(path):
        return jsonify({'Error':'File not found'}), 404 
    try:
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.call(['open',path])
        else:
            subprocess.call(['xdg-open',path])
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/open-folder')
def open_folder():
    path = request.args.get('path','')
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        return jsonify({'Error': 'Folder not found'}),404
    try:
        if sys.platform == 'win32':
            subprocess.call(['explorer', folder])
        elif sys.platform == 'darwin':
            subprocess.call(['open', folder])
        else:
            subprocess.call(['xdg-open', folder])
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    return jsonify({'total': database.get_total()})

thread = threading.Thread(target=watcher.run, daemon=True)
thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
