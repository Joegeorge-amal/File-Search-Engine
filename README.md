# 🔍 FileSearch — Local File Search Engine

A fast, lightweight local file search engine that actually works — built because Windows Search is slow and unreliable.

Search files by name or by words **inside** the file. Open them directly from your browser.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-green) ![SQLite](https://img.shields.io/badge/SQLite-3-orange)

---

## Features

- 🔎 Search by filename or content inside files
- 📄 Supports .txt, .py, .md, .pdf, .docx, .csv, .json and more
- ⚡ Instant results from a local SQLite index
- 📂 Open files or folders directly from the browser
- 🔄 Auto-updates index when files are created, modified, renamed or deleted
- 🎯 Exact filename matches ranked first in results
- 💡 Lightweight — barely uses any CPU or RAM in the background

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Joegeorge-amal/File-Search-Engine.git
cd File-Search-Engine
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Index your files (do this once)**
```bash
python indexer.py
```
This scans your Documents, Desktop, Downloads and other folders and saves everything to a local database. Takes a few minutes the first time depending on how many files you have.

**4. Start the app**
```bash
python app.py
```

**5. Open your browser**
```
http://localhost:5000
```

---

## Running it permanently (optional)

If you want FileSearch to start automatically every time your PC boots:

1. Create a file called `start.bat` in the project folder:
```bat
:loop
python app.py
goto loop
```

2. Press `Win + R`, type `shell:startup` and press Enter

3. Paste a shortcut to `start.bat` in that folder

Now FileSearch starts automatically on boot and is always available at `localhost:5000`.

---


## Customizing which folders to index

Edit the `folders_to_index` list in `indexer.py`:
```python
folders_to_index = [
    os.path.expanduser('~/OneDrive'),
    os.path.expanduser('~/Documents'),
    os.path.expanduser('~/Desktop'),
    os.path.expanduser('~/Downloads'),
    'D:/MyProjects',  # add any custom folders here
]
```

---

## Built With

- Python
- Flask
- SQLite
- Watchdog
- HTML, CSS, JavaScript
